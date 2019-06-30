import React, { Component } from "react";
import Body from "./Body.js";

class Play extends Component {
  render() {
    return <Body token={this.props.token} />;
  }
}

export default Play;
