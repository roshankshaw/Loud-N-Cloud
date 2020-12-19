import React,{useState} from 'react';
import { DropdownButton,Dropdown,ButtonGroup } from 'react-bootstrap';
import RenderMap from './../maps/populationMap';
import './../../assets/css/literacyMap.css';

class Dashboard2 extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      population:"medium",
      active:"medium",
      risk:"medium"
    };
    this.BUTTONS=[
      {type:'primary',label:'Population'},
      {type:'danger',label:'Active Cases'},
      {type:'success',label:'Risk Score'},
    ];
    this.handleClick=this.handleClick.bind(this);
    this.renderDropdownButton=this.renderDropdownButton.bind(this);
  }
  handleClick (d){
    let allNodes=d.target.parentElement.parentElement.querySelectorAll("li");
    allNodes.forEach((y)=>{y.classList.remove("active")});
    if (d.target.id=='Population'){
      this.setState({population:d.target.textContent.toLowerCase()});
      d.target.parentElement.classList.add("active");
    }
    
    if (d.target.id=='Active Cases'){
      this.setState({active:d.target.textContent.toLowerCase()});
      d.target.parentElement.classList.add("active")
    }
    
    if (d.target.id=='Risk Score'){
      this.setState({risk:d.target.textContent.toLowerCase()});
      d.target.parentElement.classList.add("active")
    }
  }
  renderDropdownButton(title, i) {
    return (
      <DropdownButton
        as={ButtonGroup}
        bsStyle={i.toLowerCase()}
        variant={i}
        title={title}
        key={i}
        id={`dropdowna`}
      >
        <Dropdown.Item eventKey="2" id= {title} onClick={this.handleClick} active>Medium</Dropdown.Item>
        <Dropdown.Item eventKey="1" id= {title}   onClick={this.handleClick}>High</Dropdown.Item>
        <Dropdown.Item eventKey="3" id= {title}  onClick={this.handleClick}>Low</Dropdown.Item>
      </DropdownButton>
    );
  }
  render() {
    return(
    <div className="content">
      <div className="container-fluid">
        <div className="row">
          <div className="col-md-4">
            <RenderMap state={this.state} />
          </div>
          <div className="col-md-4">
            {this.BUTTONS.map(button => this.renderDropdownButton(button.label,button.type))}
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
    </div>);
  };
}
export default Dashboard2;

