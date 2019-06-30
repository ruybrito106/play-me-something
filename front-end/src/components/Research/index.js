import React from "react";
import axios from "axios";

export default class Research extends React.Component {
  state = {
    data: null
  };

  componentDidMount() {
    axios
      .get(`http://localhost:5000/survey/accessToken=${this.props.token}`)
      .then(data => this.setState({ data }))
      .catch(err => console.log(err));
  }

  render() {
    console.log(this.state.data);
    return <div />;
  }
}
