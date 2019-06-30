import React from "react";
import axios from "axios";
import "./Research.css";
import SpotifyPlayer from "react-spotify-player";
import { Button, Header, Checkbox } from "semantic-ui-react";

export default class Research extends React.Component {
  state = {
    data: null,
    selected: null
  };

  componentDidMount() {
    this.handleNext();
  }

  render() {
    const { data, selected } = this.state;

    return (
      <div className="Research-root">
        <div>
          <div className="Research-box">
            <div className="Research-panel">
              <Header textAlign="center" className="Research-title">
                Choose a song that matches how this text feels like!
              </Header>
              {data && <div className="Research-text">{data.text}</div>}
            </div>
            <div className="Research-panel Research-panel2">
              {data && (
                <div>
                  {data.spotify_song_ids.map(id => (
                    <div key={id} className="Research-music">
                      <SpotifyPlayer
                        uri={`spotify:track:${id}`}
                        size={{
                          width: "100%",
                          height: 80
                        }}
                        view="list"
                        theme="black"
                      />
                      <Checkbox
                        checked={selected === id}
                        onClick={() => this.setState({ selected: id })}
                        className="Research-radio"
                        radio
                      />
                    </div>
                  ))}
                </div>
              )}
              {!data && <div />}
              <div className="Research-btns">
                <Button
                  onClick={this.handleNext}
                  className="Research-btn"
                  floated="right"
                  color="red"
                >
                  NONE MATCHES
                </Button>
                <Button
                  onClick={this.handleChoose}
                  disabled={!selected}
                  className="Research-btn"
                  floated="right"
                  primary
                >
                  CHOOSE
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  handleChoose = () => {
    const {
      selected,
      data: { text_id }
    } = this.state;
    axios
      .post(`http://localhost:5000/survey`, {
        text_id,
        spotify_song_id: selected
      })
      .then(this.handleNext())
      .catch(err => console.log(err));
  };

  handleNext = () => {
    this.setState({ data: null, selected: null }, () =>
      axios
        .get(`http://localhost:5000/survey`)
        .then(({ data }) => this.setState({ data }))
        .catch(err => console.log(err))
    );
  };
}
