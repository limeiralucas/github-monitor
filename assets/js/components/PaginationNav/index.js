import React from 'react';
import PropTypes from 'prop-types';
import { nanoid } from 'nanoid';

import PageItem from './PageItem';

const PaginationNav = ({ currentPage, totalPages }) => {
  if (!totalPages || totalPages < 2) return null;

  const pageItems = Array.from({ length: totalPages }).map(
    (_, index) => (
      <PageItem
        active={(index + 1) === currentPage}
        page={index + 1}
        key={nanoid()}
      />
    ),
  );

  return (
    <div className="d-flex justify-content-center">
      <nav aria-label="Page navigation">
        <ul className="pagination">
          <PageItem page={currentPage - 1} text="Previous" disabled={currentPage === 1} />
          {pageItems}
          <PageItem page={currentPage + 1} text="Next" disabled={currentPage === totalPages} />
        </ul>
      </nav>
    </div>
  );
};

PaginationNav.propTypes = {
  currentPage: PropTypes.number.isRequired,
  totalPages: PropTypes.number.isRequired,
};

export default PaginationNav;
