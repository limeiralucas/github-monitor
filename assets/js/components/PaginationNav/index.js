import React from 'react';
import PropTypes from 'prop-types';

const PaginationNav = ({ currentPage, totalPages, onPageChange }) => {
  const pageItems = Array.from({ length: totalPages }).map(
    (_, index) => (
      <li className="page-item">
        <button type="button" className={`page-link page-button ${(index + 1) === currentPage && 'active'}`} onClick={() => onPageChange(index + 1)}>
          {index + 1}
        </button>
      </li>
    ),
  );

  return (
    <div className="d-flex justify-content-center">
      <nav aria-label="Page navigation">
        <ul className="pagination">
          <li className="page-item">
            <button type="button" className="page-link">Previous</button>
          </li>
          {pageItems}
          <li className="page-item">
            <button type="button" className="page-link">Next</button>
          </li>
        </ul>
      </nav>
    </div>
  );
};

PaginationNav.propTypes = {
  currentPage: PropTypes.number.isRequired,
  totalPages: PropTypes.number.isRequired,
  onPageChange: PropTypes.func.isRequired,
};

export default PaginationNav;
