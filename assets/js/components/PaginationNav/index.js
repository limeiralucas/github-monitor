import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

const PaginationNav = ({ currentPage, totalPages, searchParams }) => {
  const getUrlWithParam = (paramName, value) => {
    const updatedSearchParams = new URLSearchParams(searchParams);
    updatedSearchParams.set(paramName, value);

    return updatedSearchParams.toString();
  };

  const pageItems = Array.from({ length: totalPages }).map(
    (_, index) => (
      <li className={`page-item page-number ${(index + 1) === currentPage && 'active'}`}>
        <Link to={`/?${getUrlWithParam('page', index + 1)}`} className="page-link">{index + 1}</Link>
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
  searchParams: PropTypes.string.isRequired,
};

export default PaginationNav;
