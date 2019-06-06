import React, { Component } from 'react';
import './Body.css';
import Panel from './Panel.js'

class Body extends Component {
    render() {
        return (
            <div className="Body-root">
                <Panel />
            </div>
        );
    }
}

export default Body;