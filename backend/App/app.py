from flask import Flask
from flask import jsonify,after_this_request,make_response
import json, ast
import sqlquery as query
from flask_cors import CORS, cross_origin
# import pandas as pd
app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False


@app.route('/getRows',methods=['GET'])
def getRows():
	all_rows, column_names=query.getRows('./database/results.db')
	res=[{column_names[i]:row[i] for i in range(len(row))} for row in all_rows]
	res={r['detecteddistrict']:r for r in res}
	return jsonify(res)

@app.route('/getRowsSortByCol/<column_json>',methods=['GET'])
def getRowsSortByCol(column_json):
    column_dict={}
    try:
        column_dict=ast.literal_eval(column_json)
    except BaseException as e:
        print(f'{column_json}>>>>>>>>>>>>>>>>>>>{e}')
    
    all_rows, column_names=query.getRows('./database/results.db')
    res=[{column_names[i]:row[i] for i in range(len(row))} for row in all_rows]
    for col in reversed(list(column_dict.keys())):
    	res=sorted(res, key=lambda k: k[col], 
                reverse=False if column_dict[col]=='ascend' else True)
    res={r['detecteddistrict']:r for r in res}
    for i, r in enumerate(res):
    	res[r]['index']=i+1
    return jsonify(res)

@app.route('/getCols')
def getCols():
	column_names=query.getCols('./database/results.db')
	return jsonify(column_names)

@app.route('/getCount')
def getCount():
    rows, column_names = query.getCount('./database/results.db')
    counts = map(sum, list(zip(*rows)))

    res={col:count for col, count in zip(column_names, counts)}
    print(res)
    return jsonify(res)

# @app.route('/getFilteredColumns/<column_json>',methods=['GET'])
# def getFilteredColumns(column_json):
#     column_dict={}
#     try:
#         column_dict=ast.literal_eval(column_json)
#     except BaseException as e:
#         print(f'{column_json}>>>>>>>>>>>>>>>>>>>{e}')
    
#     all_rows, column_names=query.getCount('./database/results.db')
#     df=pd.DataFrame(all_rows, columns=column_names)
#     for col, val in column_dict.items():
#     	df=df[df[f'Binary_{col}']==val]
#     res={r['detecteddistrict']:r for r in df.to_dict('records')}
#     for i, r in enumerate(res):
#     	res[r]['index']=i+1
#     return jsonify(res)

@app.route('/')
def hello_name():
    resp={"APIs" : {"sorted":"/getRowsSortByCol/%7B%22confirmed%22:%22ascend%22,%20%22active%22:%22ascend%22%7D", 
    "all rows":"/getRows",
    "columns info":"/getCols",
    "total count":"/getCount",
    "filter columns":"/getFilteredColumns/%7B%22Population%22:1%7D"}}
    return jsonify(resp)

if __name__ == '__main__':
#    app.config['db_path']='../database/results.db'
	app.run(threaded=True, port=5000)
