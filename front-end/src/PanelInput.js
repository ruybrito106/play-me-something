import React, { Component } from 'react';
import './PanelInput.css';
import TextField from '@material-ui/core/TextField';
import formState from './formState.js';

class PanelInput extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="PanelInput-root">
                <TextField 
                    variant='outlined' 
                    multiline={true}
                    helperText='This text will determine which song will be playing below'
                    label='Text'
                    placeholder='Start by typing something...'
                    rows='13'
                    style={{width: '100%'}}
                    disabled={this.props.formState === formState.SUBMITTED}
                    onChange={event => this.props.onTextChange(event.target.value)}
                />
            </div>
        );
    }
}

export default PanelInput;