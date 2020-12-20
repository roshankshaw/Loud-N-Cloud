import React from 'react';
import RenderMap from './../maps/clusterMap';
import './../../assets/css/literacyMap.css';

const Dashboard3 = () => (
  <div className="content">
    <div className="container-fluid">
      <div className="row">
        <div className="col-md-4">
          <RenderMap />
        </div>
      </div>
      {/* <div className="row">
        <div className="col-md-6">
          <UserBehaviorChart />
        </div>
        <div className="col-md-6">
          <Tasks />
        </div>
      </div> */}

    </div>
  </div>
);

export default Dashboard3;