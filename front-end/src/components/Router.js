import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect
} from "react-router-dom";
import Play from "./Play";
import Research from "./Research";
import Navbar from "./Navbar";
import "./Router.css";

const authEndpoint = "https://accounts.spotify.com/authorize";
const clientId = "15dd89009cfa4dcb9f0fdbb330518807";
const redirectUri = "http://localhost:3000/";
const scopes = ["user-read-currently-playing", "user-read-playback-state"];
const loginURL = `${authEndpoint}/?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scopes.join(
  "%20"
)}&response_type=token&show_dialog=true`;

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

export default class AppRouter extends React.Component {
  componentDidMount() {
    if (hash.access_token) {
      this.setState(
        { token: hash.access_token },
        () => (window.location.hash = "")
      );
    } else {
      window.location = loginURL;
    }
  }

  state = {
    token: null
  };

  render() {
    const { token } = this.state;

    return (
      <Router>
        <Navbar />
        <div className="app">
          <Switch>
            <Route path="/" exact render={() => <Play token={token} />} />
            <Route path="/research" render={() => <Research token={token} />} />
            <Redirect to="/" />
          </Switch>
        </div>
      </Router>
    );
  }
}
