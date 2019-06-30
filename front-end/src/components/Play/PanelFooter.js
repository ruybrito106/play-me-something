import React, { Component } from 'react';
import './PanelFooter.css';
import { withStyles } from '@material-ui/core/styles';
import Button from "@material-ui/core/Button";
import formState from './formState.js';

const SubmitButton = withStyles(theme => ({
    root: {
      color: '#ffffff',
      backgroundColor: '#ffa9a8',
      '&:hover': {
        backgroundColor: '#f29291',
      },
    },
}))(Button);

const ImportButton = withStyles(theme => ({
    root: {
      color: '#ffffff',
      backgroundColor: '#a3a8af',
      '&:hover': {
        backgroundColor: '#70747a',
      },
    },
}))(Button);

class PanelFooter extends Component {
    constructor(props) {
      super(props);
	}
	
	changeState() {
		const nxtState = this.props.formState === formState.EDITION ? formState.SUBMITTED : formState.EDITION;
		this.props.onStateChange(nxtState);

		if (nxtState === formState.SUBMITTED) {
			this.props.onSubmit();
		}
	}

    render() {
		const mainBtnText = this.props.formState === formState.EDITION ? 'SUBMIT' : 'EDIT';

        return (
            <div className="PanelFooter-root">
				<div className="PanelFooter-btn">
					<ImportButton variant="contained" color="primary">IMPORT</ImportButton>
				</div>
				<div className="PanelFooter-btn">
					<SubmitButton 
						variant="contained" 
						color="primary" 
						onClick={() => this.changeState()}>
						{mainBtnText}
					</SubmitButton>
				</div>
            </div>
        );
    }
}

export default PanelFooter;