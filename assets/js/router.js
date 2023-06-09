import React from 'react';
import {
  Link, BrowserRouter as Router, Route, Routes,
} from 'react-router-dom';
import CommitListContainer from './containers/CommitListContainer';
import RepoCreateContainer from './containers/RepoCreateContainer';

export default (
  <Router>
    <div id="wrapper" className="toggled">

      <div id="sidebar-wrapper">
        <ul className="sidebar-nav">
          <li className="sidebar-brand">
            <Link to="/">
              Github Monitor
            </Link>
          </li>
        </ul>
      </div>

      <div id="page-content-wrapper">
        <div className="container-fluid">
          <RepoCreateContainer />
          <Routes>
            <Route path="/" exact element={<CommitListContainer />} />
          </Routes>
        </div>
      </div>

    </div>
  </Router>
);
