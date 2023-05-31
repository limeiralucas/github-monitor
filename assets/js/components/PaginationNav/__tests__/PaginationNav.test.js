import React from 'react';
import { shallow } from 'enzyme';

import PaginationNav from '..';

describe('PaginationNav', () => {
  function prepare(numberOfPages = 2, currentPage = 1) {
    const totalPages = numberOfPages;
    const onPageChange = jest.fn();
    const wrapper = shallow(<PaginationNav totalPages={totalPages} onPageChange={onPageChange} currentPage={currentPage} />)

    return { onPageChange, wrapper, totalPages }
  }

  it('renders previous as first button', () => {
    const { wrapper } = prepare()
    const previousButton = wrapper.find('.page-item').first().find('.page-link');
    expect(previousButton.text()).toBe('Previous');
  });

  it('renders next as last button', () => {
    const { wrapper } = prepare();
    const nextButton = wrapper.find('.page-item').last().find('.page-link');
    expect(nextButton.text()).toBe('Next');
  });

  it.each([0, 1, 2, 3])('renders %s page buttons', (numberOfPages) => {
    const { wrapper } = prepare(numberOfPages);
    const pageButtons = wrapper.find('.page-item .page-button');
    expect(pageButtons).toHaveLength(numberOfPages);

    for (const i of Array(numberOfPages).keys()) {
      const page = (i + 1).toString();
      expect(pageButtons.at(i).find('.page-link').text()).toBe(page);
      expect(pageButtons.at(i).find('.page-link').text()).toBe(page);
    }
  });

  it('calls onPageChange when a page button is clicked', () => {
    const { wrapper, onPageChange } = prepare();
    const pageButtons = wrapper.find('.page-item .page-button');

    pageButtons.at(0).find('.page-link').simulate('click');
    expect(onPageChange).toHaveBeenCalledWith(1);

    pageButtons.at(1).find('.page-link').simulate('click');
    expect(onPageChange).toHaveBeenCalledWith(2);
  });

  it.each([1, 2, 3])('renders page button %s as active', (currentPage) => {
    const { wrapper } = prepare(currentPage, currentPage);
    const pageButtons = wrapper.find('.page-item .page-button').find('.page-link');

    const activePageButton = pageButtons.at(currentPage - 1);

    expect(activePageButton.text()).toBe(currentPage.toString());
    expect(activePageButton.hasClass("active")).toBe(true);
  })
});
