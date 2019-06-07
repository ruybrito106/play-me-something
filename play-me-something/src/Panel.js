import React, { Component } from 'react';
import axios from "axios";
import './Panel.css';
import PanelInput from './PanelInput.js';
import PanelDivider from './PanelDivider.js';
import PanelFooter from './PanelFooter.js';
import SpotifyPlayer from 'react-spotify-player';
import formState from './formState.js';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import requestState from './requestState.js';

class Panel extends Component {
    state = {
        text: "",
        track: "",
        requestState: requestState.INITIAL,
    };

    constructor(props) {
        super(props);
    }

    onSubmit() {
        if (this.state.text.length > 0) {
            this.setState({requestState: requestState.LOADING});

            axios
                .post(`http://localhost:5000/analyze/accessToken=${this.props.token}`, {text: this.state.text})
                .then(data => this.setState({track: data.data.track, requestState: requestState.INITIAL}))
                .catch(err => {
                    console.log(err);
                    return null;
                })
        }
    }

    render() {
        const displayPlayer = this.props.formState === formState.SUBMITTED && this.state.text.length > 0 && this.state.requestState === requestState.INITIAL;
        const placeholderMessage = this.state.requestState === requestState.LOADING 
            ? 'Loading track...' 
            : 'You must submit something to start listing...';

        return (
            <div className="Panel-root">
                <PanelInput 
                    formState={this.props.formState} 
                    onTextChange={_text => this.setState({text: _text})} 
                />
                <PanelDivider />
                <PanelFooter 
                    formState={this.props.formState} 
                    onStateChange={this.props.onStateChange} 
                    onSubmit={() => this.onSubmit()}
                />
                <div className="Panel-player">
                    {displayPlayer ? <SpotifyPlayer
                        uri={`spotify:track:${this.state.track}`}
                        size={{
                            width: '100%',
                            height: 80,
                        }}
                        view="list"
                        theme="black"
                    /> : <div>
                        <Paper className="Panel-placeholder">
                            <Typography component="p">
                                {placeholderMessage}
                            </Typography>
                        </Paper>
                    </div>}
                </div>
            </div>
        );
    }
}

export default Panel;