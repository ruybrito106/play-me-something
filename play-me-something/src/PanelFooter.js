import React, { Component } from 'react';
import './PanelFooter.css';
import { withStyles } from '@material-ui/core/styles';
import Button from "@material-ui/core/Button";

const PlayButton = withStyles(theme => ({
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
    render() {
        return (
            <div className="PanelFooter-root">
                <div className="PanelFooter-btn">
                    <ImportButton variant="contained" color="primary">IMPORT</ImportButton>
                </div>
                <div className="PanelFooter-btn">
                    <PlayButton variant="contained" color="primary">PLAY</PlayButton>
                </div>
            </div>
        );
    }
}

export default PanelFooter;