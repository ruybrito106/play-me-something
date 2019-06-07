import React, { Component } from 'react';
import './App.css';
import Header from './Header.js';
import Body from './Body.js';

export const authEndpoint = 'https://accounts.spotify.com/authorize';
const clientId = "CLIENT_ID";
const redirectUri = "http://localhost:3000/";
const scopes = [
  "user-read-currently-playing",
  "user-read-playback-state",
];

const hash = window.location.hash
  .substring(1)
  .split("&")
  .reduce(function(initial, item) {
    if (item) {
      var parts = item.split("=");
      initial[parts[0]] = decodeURIComponent(parts[1]);
    }
    return initial;
  }, {});

window.location.hash = "";

class App extends Component {
  constructor() {
    super();
    this.state = {token: null};
  }

  componentDidMount() {
    if (hash.access_token) {
      this.setState({token: hash.access_token});
    }
  }

  getLoginHref() {
    return `${authEndpoint}/?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scopes.join("%20")}&response_type=token&show_dialog=true`;
  }

  render() {
    return (
      <div className="App">
        <Header loginHref={this.getLoginHref()} logged={this.state.token != null} />
        <Body token={this.state.token}/>
      </div>
    );
  }
}

export default App;
