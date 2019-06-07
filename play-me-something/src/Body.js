import React, { Component } from 'react';
import './Body.css';
import Panel from './Panel.js';
import formState from './formState.js';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';

class Body extends Component {
    constructor(props) {
        super(props);
        this.state = {
            formState: formState.EDITION,
        }
    }

    render() {
        return (
            <div className="Body-root">
                {this.props.token != null && (
                    <Panel 
                        formState={this.state.formState} 
                        onStateChange={state => this.setState({formState: state})}
                        token={this.props.token}
                    />
                )}
                {this.props.token == null && (
                    <div>
                        <Paper className="Body-placeholder">
                            <Typography variant="h6" component="h4">
                                WELCOME
                            </Typography>
                            <Typography component="p">
                                You must login with Spotify to continue.
                            </Typography>
                        </Paper>
                    </div>
                )}
            </div>
        );
    }
}

export default Body;