import React, { Component } from "react";
import "./PanelFooter.css";
import { Button } from "semantic-ui-react";
import formState from "./formState.js";

class PanelFooter extends Component {
  changeState() {
    const nxtState =
      this.props.formState === formState.EDITION
        ? formState.SUBMITTED
        : formState.EDITION;
    this.props.onStateChange(nxtState);

    if (nxtState === formState.SUBMITTED) {
      this.props.onSubmit();
    }
  }

  render() {
    const mainBtnText =
      this.props.formState === formState.EDITION ? "SUBMIT" : "EDIT";

    return (
      <div className="PanelFooter-root">
        <div className="PanelFooter-btn">
          <Button primary onClick={() => this.changeState()}>
            {mainBtnText}
          </Button>
        </div>
      </div>
    );
  }
}

export default PanelFooter;
