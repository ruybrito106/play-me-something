import React, { Component } from 'react';
import './Header.css';
import logo from './logo.svg'

class Header extends Component {
    render() {
        return (
            <div className="Header-root">
                <img src={logo} className="Header-logo" alt="logo" />
                <div className="Header-title">PlayMeSomething</div>
            </div>
        );
    }
}

export default Header;