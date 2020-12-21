import React, { useState } from "react";
import { DropdownButton, Dropdown, ButtonGroup } from "react-bootstrap";
import RenderMap from "./../maps/populationMap";
import "./../../assets/css/literacyMap.css";

const initialState = { currentState: {} };
class Dashboard2 extends React.Component {
  constructor(props) {
    super(props);
    this.state = initialState;
    this.BUTTONS = [
      { type: "success", label: "Risk Score" },
      { type: "danger", label: "Active Cases" },
      { type: "primary", label: "Population" },
    ];
    this.handleClick = this.handleClick.bind(this);
    this.renderDropdownButton = this.renderDropdownButton.bind(this);
  }
  handleClick(d) {
    this.state = initialState;
    this.forceUpdate();
    let allNodes = d.target.parentElement.parentElement.parentElement.querySelectorAll(
      "a"
    );
    allNodes.forEach((y, index) => {
      y.classList.remove("active");
      if (index % 3 == 0) {
        y.classList.add("active");
      }
    });
    let allNodesInDropdown = d.target.parentElement.parentElement.querySelectorAll(
      "a"
    );
    allNodesInDropdown.forEach((y) => {
      y.classList.remove("active");
    });
    if (d.target.id == "Population") {
      if (d.target.textContent.toLowerCase() == "medium") {
        let currentState = this.state;
        delete currentState.population;
        this.setState(currentState);
      } else {
        this.setState({
          currentState: { population: d.target.textContent.toLowerCase() },
        });
      }
      d.target.classList.add("active");
    }

    if (d.target.id == "Active Cases") {
      if (d.target.textContent.toLowerCase() == "medium") {
        let currentState = this.state;
        delete currentState.active;
        this.setState(currentState);
      } else {
        this.setState({
          currentState: { active: d.target.textContent.toLowerCase() },
        });
      }
      d.target.classList.add("active");
    }

    if (d.target.id == "Risk Score") {
      if (d.target.textContent.toLowerCase() == "medium") {
        let currentState = this.state;
        delete currentState.risk;
        this.setState(currentState);
      } else {
        this.setState({
          currentState: { risk: d.target.textContent.toLowerCase() },
        });
      }
      d.target.classList.add("active");
    }
  }
  renderDropdownButton(title, i) {
    return (
      <DropdownButton
        as={ButtonGroup}
        variant={i}
        title={title}
        key={i}
        id={`dropdowna`}
      >
        <Dropdown.Item
          eventKey="2"
          id={title}
          onClick={this.handleClick}
          active
        >
          Default
        </Dropdown.Item>
        <Dropdown.Item eventKey="1" id={title} onClick={this.handleClick}>
          High
        </Dropdown.Item>
        <Dropdown.Item eventKey="3" id={title} onClick={this.handleClick}>
          Low
        </Dropdown.Item>
      </DropdownButton>
    );
  }
  render() {
    return (
      <div className="content">
        <div className="container-fluid">
          <div className="row">
            <div className="col-md-7">
              <RenderMap state={this.state} />
            </div>
            <div className="col-md-4">
              {this.BUTTONS.map((button) =>
                this.renderDropdownButton(button.label, button.type)
              )}
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
  }
}
export default Dashboard2;
