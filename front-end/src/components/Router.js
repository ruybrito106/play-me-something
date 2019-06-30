import React from "react";
import { BrowserRouter as Router, Switch, Route, Redirect } from "react-router-dom";

import Play from './Play'
import Research from './Research'

const AppRouter = () => (
    <Router>
        <Switch>
            <Route path="/" exact component={Play}/>
            <Route path="/research" component={Research}/>
            <Redirect to="/"/>
        </Switch>
    </Router>
)

export default AppRouter