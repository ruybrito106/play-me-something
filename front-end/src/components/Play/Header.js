import React, { Component } from 'react';
import './Header.css';
import { withStyles } from '@material-ui/core/styles';
import logo from './logo.svg'
import Button from "@material-ui/core/Button";

const LoginButton = withStyles(theme => ({
    root: {
      color: '#ffffff',
      backgroundColor: '#1db954',
      '&:hover': {
        backgroundColor: '#159642',
      },
    },
}))(Button);

class Header extends Component {
    render() {
        return (
            <div className="Header-root">
                <div className="Header-left">
                    <img src={logo} className="Header-logo" alt="logo" />
                    <div className="Header-title">PlayMeSomething</div>
                </div>
                <div className="Header-right">
                    {!this.props.logged && <LoginButton 
                        variant="contained" 
                        color="primary" 
                        href={this.props.loginHref}>
                        LOGIN WITH SPOTIFY
                    </LoginButton>}
                </div>
            </div>
        );
    }
}

export default Header;