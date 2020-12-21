import React from "react";
import RenderMap from "./../maps/clusterMap";
import "./../../assets/css/literacyMap.css";
import mapKey from "./../../assets/images/mapkeys/lowtohigh.jpg";

const Dashboard3 = () => (
  <div className="content">
    <div className="container-fluid">
      <div className="row">
        <div className="col-md-4">
          <RenderMap />
        </div>
        <div className="col-md-20">
          <img src={mapKey} />
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
