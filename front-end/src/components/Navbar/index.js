import React from "react";
import { Menu } from "semantic-ui-react";
import { withRouter } from "react-router";

import logo from "./logo.svg";
import "./Navbar.css";

class Navbar extends React.Component {
  render() {
    const {
      location: { pathname }
    } = this.props;

    return (
      <Menu inverted>
        <Menu.Item className="Menu-img">
          <img src={logo} className="Header-logo" alt="logo" />
        </Menu.Item>
        <Menu.Item
          name="play"
          content="Play Me Something!"
          active={pathname === "/"}
          onClick={() => this.handleItemClick("/")}
        />
        <Menu.Item
          name="survey"
          active={pathname === "/research"}
          onClick={() => this.handleItemClick("/research")}
        />
      </Menu>
    );
  }

  handleItemClick = url => {
    this.props.history.push(url);
  };
}

export default withRouter(Navbar);
