import * as types from '../actions/ActionTypes';

const initialState = {
  commits: [],
  successMessage: false,
  totalPages: 0,
  currentPage: 0,
};

const commitReducer = (state = initialState, action) => {
  switch (action.type) {
    case types.GET_COMMITS_SUCCESS:
      return {
        ...state,
        commits: Object.values(action.payload.results),
        totalPages: action.payload.total_pages,
        currentPage: action.payload.page,
      };
    case types.CREATE_REPOSITORY_SUCCESS: {
      return { ...state, successMessage: action.payload.successMessage };
    }
    default:
      return state;
  }
};

export default commitReducer;
