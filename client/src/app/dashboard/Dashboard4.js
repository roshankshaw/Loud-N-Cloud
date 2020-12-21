import React from "react";
import RenderMap from "../maps/casesMap";
import "./../../assets/css/literacyMap.css";

const Dashboard4 = () => (
  <div className="content">
    <div className="container-fluid">
      <div className="row">
        <div className="col-md-4">
          <RenderMap />
        </div>
        {/* <div className="col-md-8">
          <SalesChart />
        </div> */}
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

export default Dashboard4;
