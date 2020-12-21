#!/usr/bin/env python
# coding: utf-8

# ## Imports

# In[5]:


import pandas as pd, requests
import numpy as np
import pandas as pd
import scipy
pd.options.mode.chained_assignment = None  # default='warn'

from tqdm import tqdm

import matplotlib.pyplot as plt
plt.style.use('dark_background')

import matplotlib.dates as mdates
# %matplotlib inline 

import mpld3
# mpld3.enable_notebook()

from scipy.integrate import odeint
import lmfit
from lmfit.lineshapes import gaussian, lorentzian

import warnings
warnings.filterwarnings('ignore')

import sqlite3, os
from sklearn.preprocessing import MinMaxScaler


# ## Parse Current District Cases

# In[5]:


def parseDistrictData(url, json_column, drop_columns):   
    
    # fetch json
    jsonData = requests.get(url).json()
    
    # extract data from json into dataframe
    districtsDfList=[]
    
    for statename, stateData in jsonData.items():
        
        stateDf=pd.DataFrame(stateData)
        # normalize json columns and split them into individual columns
        flattenedDf=pd.json_normalize(stateDf[json_column])
        stateDf.drop(columns=[json_column], inplace=True)
        flattenedDf.index=stateDf.index
        stateDf[flattenedDf.columns]=flattenedDf[flattenedDf.columns]
        if len(drop_columns):
            stateDf.drop(columns=drop_columns, inplace=True)
        stateDf.statecode=statename
        districtsDfList.append(stateDf)    
    
    # final dataframe
    districtsDf=pd.concat(districtsDfList)
    districtsDf['detecteddistrict']=districtsDf.index
    districtsDf.reset_index(inplace=True, drop=True)    
    
    districtsDf['detecteddistrict']=districtsDf['detecteddistrict'].str.lower()
    districtsDf['statecode']=districtsDf['statecode'].str.lower()
    
#     coronaDf.set_index(["statecode", "Constituency"], inplace = True,
#                             append = False, drop = True, verify_integrity=True)


#     # drop row if active case is negative, nan or infinity
#     coronaDf=coronaDf[coronaDf.active>=0]
#     coronaDf=coronaDf[np.isfinite(coronaDf.active)]
#     coronaDf=coronaDf[~coronaDf.active.isna()]
    
    # coronaDf.to_excel('hack.xlsx')
    return districtsDf


# In[6]:


API='https://api.covid19india.org/state_district_wise.json'

currentDistrictCasesDf=parseDistrictData(url=API, json_column='districtData', 
                        drop_columns=['notes', 'delta.confirmed', 'delta.deceased', 'delta.recovered'])


# In[36]:


currentDistrictCasesDf=currentDistrictCasesDf.drop(columns=['statecode'])


# In[104]:


timeseriesData=pd.concat(
[pd.DataFrame(requests.get(f'https://api.covid19india.org/raw_data{i}.json').json()['raw_data']) 
 for i in range(1, 18)])
timeseriesData['dateannounced']=pd.to_datetime(timeseriesData['dateannounced'])
timeseriesData=timeseriesData[timeseriesData['numcases']!='']
timeseriesData['numcases']=timeseriesData['numcases'].astype(int)
timeseriesData.to_excel('data/covid.xlsx')


# ## Time Series data fetch

# In[105]:


timeseriesData=pd.read_excel('data/covid.xlsx', usecols=[
'nationality', 'detectedstate', 'detecteddistrict',
'agebracket', 'dateannounced', 'numcases', 'currentstatus'], parse_dates=["dateannounced"])


# In[106]:


timeseriesData=timeseriesData[['nationality', 'detectedstate', 'detecteddistrict',
'agebracket', 'currentstatus', 'dateannounced', 'numcases']]


# In[107]:


IndianStates=["Andaman and Nicobar Islands","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadra and Nagar Haveli","Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"]
IndianStates=list(map(lambda state: state.lower(), IndianStates))


# In[108]:


timeseriesData['detectedstate']=timeseriesData['detectedstate'].str.lower()
timeseriesData['detecteddistrict']=timeseriesData['detecteddistrict'].str.lower()


# In[109]:


timeseriesData=timeseriesData[(timeseriesData.detectedstate.isin(IndianStates)) | (timeseriesData.nationality=='India')]
timeseriesData=timeseriesData[timeseriesData.currentstatus=='Deceased']


# In[110]:


listOfDistrictData={(state, district):distdf.groupby('dateannounced').agg(deaths=('numcases', sum)).cumsum()
          for (state, district), distdf in timeseriesData.groupby(['detectedstate', 'detecteddistrict'])}


# In[ ]:





# # Important
# 
# ## The model is capable of tackling vaccination scenario, by simply decreasing the susceptibles by subtracting the number of vaccinated, but because vaccination is zero currently, so that calculation won't be reflected on the values

# In[2]:


vaccinated = 0


# In[ ]:





# In[ ]:





# ## Census Data

# In[111]:


rawcensusDf=pd.read_csv('data/census-2011.csv')
rawcensusDf['District name']=rawcensusDf['District name'].str.lower()
rawcensusDf['detecteddistrict']=rawcensusDf['District name']
rawcensusDf.drop(columns=['State name', 'District name'], inplace=True)
rawcensusData=dict(zip(rawcensusDf['detecteddistrict'], rawcensusDf['Population']))


IndiaDistricts=[district for _, district in listOfDistrictData]

censusDf=pd.DataFrame([(district, rawcensusData.get(district, None)) for district in IndiaDistricts], 
                      columns=['detecteddistrict', 'Population'])

censusDf=censusDf.fillna(censusDf.mean())
censusData=dict(zip(censusDf['detecteddistrict'], censusDf['Population']))


# ## Model

# In[112]:


## some necessary settings for SIR model working


riskForesightPeriod=15 # cases after 15 days will be considered as risk

beds = pd.read_csv("data/beds.csv", header=0)
agegroups = pd.read_csv("data/agegroups.csv")
probabilities = pd.read_csv("data/probabilities.csv")

# create some dicts for fast lookup
# 1. beds
beds_lookup = dict(zip(beds["Country"], beds["ICU_Beds"]))
# 2. agegroups
agegroup_lookup = dict(zip(agegroups['Location'], agegroups[['0_9', '10_19', '20_29', '30_39', '40_49', '50_59', '60_69', '70_79', '80_89', '90_100']].values))

# store the probabilities collected
prob_I_to_C_1 = list(probabilities.prob_I_to_ICU_1.values)
prob_I_to_C_2 = list(probabilities.prob_I_to_ICU_2.values)
prob_C_to_Death_1 = list(probabilities.prob_ICU_to_Death_1.values)
prob_C_to_Death_2 = list(probabilities.prob_ICU_to_Death_2.values)



#parameters tuning

gamma = 1.0/9.0
sigma = 1.0/3.0

agegroups = agegroup_lookup["India"]
beds_per_100k = beds_lookup["India"]
outbreak_shift = 30
params_init_min_max = {"R_0_start": (3.0, 2.0, 5.0), "k": (2.5, 0.01, 5.0), "x0": (90, 0, 120), "R_0_end": (0.9, 0.3, 3.5),
                       "prob_I_to_C": (0.05, 0.01, 0.1), "prob_C_to_D": (0.5, 0.05, 0.8),
                       "s": (0.003, 0.001, 0.01)}



#functions definition

def deriv(y, t, beta, gamma, sigma, N, p_I_to_C, p_C_to_D, Beds):
    S, E, I, C, R, D = y

    # vaccinated are being considered here
    dSdt = -beta(t) * I * (S-vaccinated) / N
    dEdt = beta(t) * I * (S-vaccinated) / N - sigma * E
    dIdt = sigma * E - 1/12.0 * p_I_to_C * I - gamma * (1 - p_I_to_C) * I
    dCdt = 1/12.0 * p_I_to_C * I - 1/7.5 * p_C_to_D * min(Beds(t), C) - max(0, C-Beds(t)) - (1 - p_C_to_D) * 1/6.5 * min(Beds(t), C)
    dRdt = gamma * (1 - p_I_to_C) * I + (1 - p_C_to_D) * 1/6.5 * min(Beds(t), C)
    dDdt = 1/7.5 * p_C_to_D * min(Beds(t), C) + max(0, C-Beds(t))
    return dSdt, dEdt, dIdt, dCdt, dRdt, dDdt


def logistic_R_0(t, R_0_start, k, x0, R_0_end):
    return (R_0_start-R_0_end) / (1 + np.exp(-k*(-t+x0))) + R_0_end

def Model(days, N, beds_per_100k, R_0_start, k, x0, R_0_end, prob_I_to_C, prob_C_to_D, s):

    def beta(t):
        return logistic_R_0(t, R_0_start, k, x0, R_0_end) * gamma
    
    def Beds(t):
        beds_0 = beds_per_100k / 100_000 * N
        return beds_0 + s*beds_0*t  # 0.003

    y0 = N-1.0, 1.0, 0.0, 0.0, 0.0, 0.0
    t = np.linspace(0, days-1, days)
    ret = odeint(deriv, y0, t, args=(beta, gamma, sigma, N, prob_I_to_C, prob_C_to_D, Beds))
    S, E, I, C, R, D = ret.T
    R_0_over_time = [beta(i)/gamma for i in range(len(t))]

    return t, S, E, I, C, R, D, R_0_over_time, Beds, prob_I_to_C, prob_C_to_D

def fitter(x, R_0_start, k, x0, R_0_end, prob_I_to_C, prob_C_to_D, s):
    ret = Model(days, districtPopulation, beds_per_100k, R_0_start, k, x0, R_0_end, prob_I_to_C, prob_C_to_D, s)
    return ret[6][x]


# ## Fitting each district data

# In[ ]:


predictions=[]

for (state, district), districtDf in tqdm(listOfDistrictData.items()):
    
    data = districtDf.reset_index()["deaths"].values
    
    days = outbreak_shift + len(data)
    if outbreak_shift >= 0:
        y_data = np.concatenate((np.zeros(outbreak_shift), data))
    else:
        y_data = y_data[-outbreak_shift:]

    x_data = np.linspace(0, days - 1, days, dtype=int)
    
    # parameters
    districtPopulation=censusData[district]
    mod = lmfit.Model(fitter)

    for kwarg, (init, mini, maxi) in params_init_min_max.items():
        mod.set_param_hint(str(kwarg), value=init, min=mini, max=maxi, vary=True)

    params = mod.make_params()
    fit_method = "leastsq"
#     result.plot_fit(datafmt="-")

    parameters=mod.fit(y_data, params, method="least_squares", x=x_data).best_values.values()
    ret=Model(days+riskForesightPeriod, districtPopulation, beds_per_100k, *(parameters))
    pred, susceptible=ret[3][-1], ret[1][-1]
    predictions.append([state, district, pred, districtPopulation, susceptible])


# In[ ]:


riskDf=pd.DataFrame(predictions, columns=['State', 'detecteddistrict', 
                                          'Active Cases Predicted', 'Population', 'Susceptibles'])


# ## Add current cases data to dataframe

# In[ ]:


finalDf=pd.merge(riskDf, currentDistrictCasesDf, on='detecteddistrict', how='left')

finalDf.to_excel('data/intermediate.xlsx')


# ## Color Logic

# In[6]:


def getcolor(value):
    r=int(value*255)
    g=255-int(r)
    b=127
    return ' '.join([str(r), str(g), str(b)])


# ## Risk Estimation

# In[8]:


finalDf=pd.read_excel('data/intermediate.xlsx')

finalDf['New Active Cases Predicted'] = finalDf['Active Cases Predicted']-finalDf['active']
finalDf['New Active Cases Predicted'] = finalDf['New Active Cases Predicted'].fillna(value=0)
finalDf['New Active Cases Predicted'] = finalDf['New Active Cases Predicted'].apply(lambda x : 0 if x<0 else x)
finalDf['Normalized Risk'] = MinMaxScaler().fit_transform(finalDf[['New Active Cases Predicted']])
finalDf['Log Risk'] = finalDf['New Active Cases Predicted'].apply(lambda x : np.log2(1+x))
finalDf['Normalized Log Risk'] = MinMaxScaler().fit_transform(finalDf[['Log Risk']])
finalDf['Vaccination Priority'] = finalDf['Susceptibles'] * finalDf['Normalized Risk']
finalDf['Normalized Vaccination Priority'] = MinMaxScaler().fit_transform(finalDf[['Vaccination Priority']])

finalDf['Color of Normalized Risk']=finalDf['Normalized Risk'].apply(lambda x : getcolor(x))
finalDf['Color of Normalized Vaccination Priority']=finalDf['Normalized Vaccination Priority'].apply(lambda x : getcolor(x))

finalDf['Normalized active'] = MinMaxScaler().fit_transform(finalDf[['active']])
finalDf['Normalized confirmed'] = MinMaxScaler().fit_transform(finalDf[['confirmed']])
finalDf['Normalized recovered'] = MinMaxScaler().fit_transform(finalDf[['recovered']])
finalDf['Normalized deceased'] = MinMaxScaler().fit_transform(finalDf[['deceased']])
finalDf['vaccinated']=0
finalDf['Relative Vaccination Priority'] = finalDf['Normalized Vaccination Priority'] / finalDf['Normalized Vaccination Priority'].sum()


# In[3]:


# binaryColumns=[
#  'Active Cases Predicted',
#  'Population',
#  'Susceptibles',
#  'active',
#  'confirmed',
#  'deceased',
#  'recovered',
#  'New Active Cases Predicted',
#  'Normalized Risk',
#  'Log Risk',
#  'Normalized Log Risk',
#  'Vaccination Priority',
#  'Normalized Vaccination Priority',
#  'Normalized active',
#  'Normalized confirmed',
#  'Normalized recovered',
#  'Normalized deceased',
#  'Relative Vaccination Priority']

# for col in binaryColumns:
#     mean, _ = scipy.stats.distributions.norm.fit(finalDf[col])
#     finalDf[f'Binary {col}']=(finalDf[col] > mean).astype(int)


# In[9]:


finalDf.columns = list(map(lambda x : x.replace(' ', '_'), finalDf.columns))
finalDf.to_excel('data/results.xlsx', index=False)


# ## Storing results into database

# In[10]:


if not os.path.isdir('database'):
    os.makedirs('database')

cnx = sqlite3.connect('database/results.db')
finalDf.to_sql(name='main', con=cnx, if_exists='replace')
cnx.close()

