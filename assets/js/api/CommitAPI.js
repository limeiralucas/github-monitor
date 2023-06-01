import axios from 'axios';
import { reset } from 'redux-form';

import store from '../store';
import {
  createRepositorySuccess, getCommitsSuccess,
} from '../actions/CommitActions';

export const getCommits = (params = {}) => axios.get('/api/commits/', { params })
  .then((response) => {
    store.dispatch(getCommitsSuccess({ ...response.data }));
  });

export const createRepository = (values, headers, formDispatch) => axios.post('/api/repositories/', values, { headers })
  .then((response) => {
    store.dispatch(createRepositorySuccess(response.data, true));
    formDispatch(reset('repoCreate'));
  }).catch((error) => {
    const err = error.response;
    console.log(err);
  });
