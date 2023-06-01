import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { useSearchParams } from 'react-router-dom';

import * as commitAPI from '../api/CommitAPI';
import CommitList from '../components/CommitList';
import PaginationNav from '../components/PaginationNav';

const CommitListContainer = ({ commits, totalPages, currentPage }) => {
  const [searchParams] = useSearchParams();
  const searchParamsString = searchParams.toString();
  const filters = {
    author: searchParams.get('author'),
    repository: searchParams.get('repository'),
    page: searchParams.get('page'),
  };

  useEffect(() => {
    commitAPI.getCommits(filters);
  }, Object.values(filters));

  return (
    <div>
      <CommitList commits={commits} searchParams={searchParamsString} />
      <PaginationNav
        totalPages={totalPages}
        currentPage={currentPage}
        searchParams={searchParamsString}
      />
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
  totalPages: PropTypes.number.isRequired,
  currentPage: PropTypes.number.isRequired,
};

const mapStateToProps = (store) => ({
  commits: store.commitState.commits,
  totalPages: store.commitState.totalPages,
  currentPage: store.commitState.currentPage,
});

export default connect(mapStateToProps)(CommitListContainer);
