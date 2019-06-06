import React, { Component } from 'react';
import './Panel.css';
import PanelInput from './PanelInput.js';
import PanelDivider from './PanelDivider.js';
import PanelFooter from './PanelFooter.js';

class Panel extends Component {
    render() {
        return (
            <div className="Panel-root">
                <PanelInput />
                <PanelDivider />
                <PanelFooter />
            </div>
        );
    }
}

export default Panel;