import React from 'react';
import PropTypes from 'prop-types';
import { Link, useSearchParams } from 'react-router-dom';

const PageItem = ({
  page, text, active, disabled,
}) => {
  const [searchParams] = useSearchParams();

  const getUrlWithParam = (paramName, value) => {
    const updatedSearchParams = new URLSearchParams(searchParams);
    updatedSearchParams.set(paramName, value);

    return updatedSearchParams.toString();
  };

  let stateClass = '';
  if (disabled) {
    stateClass = 'disabled';
  } else if (active) {
    stateClass = 'active';
  }

  return (
    <li className={`page-item ${stateClass}`}>
      <Link to={!disabled && `/?${getUrlWithParam('page', page)}`} className="page-link">{text || page}</Link>
    </li>
  );
};

PageItem.propTypes = {
  page: PropTypes.number.isRequired,
  text: PropTypes.string,
  active: PropTypes.bool,
  disabled: PropTypes.bool,
};

PageItem.defaultProps = {
  text: '',
  active: false,
  disabled: false,
};

export default PageItem;
