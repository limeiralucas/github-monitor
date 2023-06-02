import React from 'react';
import { shallow } from 'enzyme';

import PaginationNav from '..';
import PageItem from '../PageItem';

describe('PaginationNav', () => {
  it.each([
    [2],
    [3],
    [4],
  ])('renders %s page items', (totalPages) => {
    const wrapper = shallow(<PaginationNav currentPage={1} totalPages={totalPages} />);
    const pageItems = wrapper.find(PageItem).slice(1, totalPages + 1);

    expect(pageItems).toHaveLength(totalPages);

    pageItems.forEach((pageItem, index) => {
      const expectedPage = index + 1;

      expect(pageItem.prop('page')).toBe(expectedPage);
    });
  });

  it.each([
    [1],
    [2],
    [3],
  ])('renders page item as active for current page %s', (currentPage) => {
    const totalPages = 10;
    const wrapper = shallow(<PaginationNav currentPage={currentPage} totalPages={totalPages} />);
    const pageItems = wrapper.find(PageItem).slice(1, totalPages + 1);
    const activePageItem = pageItems.at(currentPage - 1);

    expect(activePageItem.prop('active')).toBe(true);
    expect(activePageItem.prop('page')).toBe(currentPage);
  });

  it('renders next and previous buttons as first and last ones', () => {
    const totalPages = 5;
    const currentPage = 2;

    const wrapper = shallow(<PaginationNav currentPage={currentPage} totalPages={totalPages} />);
    const pageItems = wrapper.find(PageItem);

    const previous = pageItems.first();
    const next = pageItems.last();

    expect(previous.props()).toMatchObject({
      page: currentPage - 1,
      text: "Previous",
    });
    expect(next.props()).toMatchObject({
      page: currentPage + 1,
      text: "Next",
    })
  });

  it('does not render the component if totalPages is less than 2', () => {
    const wrapper = shallow(<PaginationNav currentPage={1} totalPages={1} />);
    const paginationNav = wrapper.find('.pagination');

    expect(paginationNav.exists()).toBe(false);
  });

  it('disables previous button when currentPage is 1', () => {
    const wrapper = shallow(<PaginationNav currentPage={1} totalPages={5} />);
    const previousButton = wrapper.find(PageItem).at(0);

    expect(previousButton.prop('disabled')).toBe(true);
  });

  it('disables next button when currentPage is the last page', () => {
    const wrapper = shallow(<PaginationNav currentPage={5} totalPages={5} />);
    const nextButton = wrapper.find(PageItem).at(6);

    expect(nextButton.prop('disabled')).toBe(true);
  });
});
