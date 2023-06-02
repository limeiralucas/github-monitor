import React from 'react';
import { shallow } from 'enzyme';
import PageItem from '../PageItem';

describe('PageItem', () => {
  beforeEach(() => {
    jest.resetAllMocks();
    jest.spyOn(require('react-router-dom'), 'useSearchParams').mockImplementation(() => []);
  })

  it('renders the page number', () => {
    const page = 1;
    const wrapper = shallow(<PageItem page={page} />);
    const pageNumber = wrapper.find('.page-link');

    expect(pageNumber.text()).toBe(page.toString());
  });

  it('renders the custom text', () => {
    const customText = 'Custom text';
    const wrapper = shallow(<PageItem page={1} text={customText} />);
    const pageLink = wrapper.find('.page-link');

    expect(pageLink.text()).toBe(customText);
  });

  it('adds the "active" class when active prop is true', () => {
    const wrapper = shallow(<PageItem page={1} active />);
    const pageItem = wrapper.find('.page-item');

    expect(pageItem.hasClass('active')).toBe(true);
  });

  it('adds the "disabled" class when disabled prop is true', () => {
    const wrapper = shallow(<PageItem page={1} disabled />);
    const pageItem = wrapper.find('.page-item');

    expect(pageItem.hasClass('disabled')).toBe(true);
  });

  it.each([
    [{}, 2, '/?page=2'],
    [{'author': 'user'}, 2, '/?author=user&page=2'],
    [{'author': 'user', 'repository': 'repo'}, 2, '/?author=user&repository=repo&page=2'],
  ])('generate url with query params and page (params: %s, page: %s)', (params, page, expectedUrl) => {
    const mockSearchParams = new URLSearchParams();

    for (const key in params) {
      mockSearchParams.set(key, params[key]);
    }

    const useSearchParamsMock = jest.fn().mockReturnValue([mockSearchParams]);
    jest.spyOn(require('react-router-dom'), 'useSearchParams').mockImplementation(useSearchParamsMock);

    const wrapper = shallow(<PageItem page={page} />);
    const link = wrapper.find('Link');
    expect(link.prop('to')).toBe(expectedUrl);
  });

  it('does not generate URL when disabled is true', () => {
    const wrapper = shallow(<PageItem page={1} disabled />);
    const link = wrapper.find('Link');
    expect(link.prop('to')).toBe(false);
  });
});
