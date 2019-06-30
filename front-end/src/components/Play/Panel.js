import React, { Component } from "react";
import axios from "axios";
import "./Panel.css";
import { Loader } from "semantic-ui-react";
import PanelInput from "./PanelInput.js";
import PanelFooter from "./PanelFooter.js";
import SpotifyPlayer from "react-spotify-player";
import formState from "./formState.js";
import requestState from "./requestState.js";

class Panel extends Component {
  state = {
    text: "",
    track: "",
    requestState: requestState.INITIAL
  };

  onSubmit() {
    if (this.state.text.length > 0) {
      this.setState({ requestState: requestState.LOADING });

      axios
        .post(`http://localhost:5000/analyze`, {
          text: this.state.text
        })
        .then(data =>
          this.setState({
            track: data.data.track,
            requestState: requestState.INITIAL
          })
        )
        .catch(err => {
          this.setState({ requestState: requestState.INITIAL });
          console.log(err);
          return null;
        });
    }
  }

  render() {
    const displayPlayer =
      this.props.formState === formState.SUBMITTED &&
      this.state.text.length > 0 &&
      this.state.requestState === requestState.INITIAL;

    return (
      <div className="Panel-root">
        <PanelInput
          formState={this.props.formState}
          onTextChange={_text => this.setState({ text: _text })}
        />
        <PanelFooter
          formState={this.props.formState}
          onStateChange={this.props.onStateChange}
          onSubmit={() => this.onSubmit()}
        />
        <div className="Panel-player">
          {displayPlayer ? (
            <SpotifyPlayer
              uri={`spotify:track:${this.state.track}`}
              size={{
                width: "100%",
                height: 80
              }}
              view="list"
              theme="black"
            />
          ) : (
            this.state.requestState === requestState.LOADING && (
              <div className="Panel-player-ld">
                <Loader active inline="centered" />
              </div>
            )
          )}
        </div>
      </div>
    );
  }
}

export default Panel;
