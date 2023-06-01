import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { useLocation } from 'react-router-dom';

import * as commitAPI from '../api/CommitAPI';
import CommitList from '../components/CommitList';

const CommitListContainer = ({ commits }) => {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const filters = {
    author: searchParams.get('author'),
    repository: searchParams.get('repository')
  };

  useEffect(() => {
    commitAPI.getCommits(filters);
  }, Object.values(filters));

  return (
    <div>
      <CommitList commits={commits} />
    </div>
  );
};

CommitListContainer.propTypes = {
  commits: PropTypes.arrayOf(PropTypes.shape({
    sha: PropTypes.string.isRequired,
    author: PropTypes.string.isRequired,
    message: PropTypes.string.isRequired,
    repository: PropTypes.string.isRequired,
    avatar: PropTypes.string,
  })).isRequired,
};

const mapStateToProps = (store) => ({
  commits: store.commitState.commits,
});

export default connect(mapStateToProps)(CommitListContainer);
