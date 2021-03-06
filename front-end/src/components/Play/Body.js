import React, { Component } from "react";
import "./Body.css";
import Panel from "./Panel.js";
import formState from "./formState.js";

class Body extends Component {
  constructor(props) {
    super(props);
    this.state = {
      formState: formState.EDITION
    };
  }

  render() {
    return (
      <div className="Body-root">
        <Panel
          formState={this.state.formState}
          onStateChange={state => this.setState({ formState: state })}
          token={this.props.token}
        />
      </div>
    );
  }
}

export default Body;
