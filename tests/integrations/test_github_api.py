from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytest

from integrations.github_api import GithubAPIClient


class TestGithubAPIClient(TestCase):
    def setUp(self) -> None:
        self.access_token = 'access-token'
        self.gh_client = GithubAPIClient(self.access_token)

    @patch('integrations.github_api.Github')
    def test_client_initialization(self, GithubClientMock):
        access_token = 'token'
        client = GithubAPIClient(access_token)

        assert client
        GithubClientMock.assert_called_once_with(access_token)

    @patch('github.Github.get_repo')
    def test_get_repository(self, get_repo_mock):
        repository_name = 'user/repo'

        repo_mock = MagicMock()
        repo_mock.name = repository_name
        get_repo_mock.return_value = repo_mock

        repo = self.gh_client.get_repository(repository_name)

        get_repo_mock.assert_called_once_with(repository_name)
        assert repo == repo_mock

    @patch('github.Github.get_repo', side_effect=Exception("Repository not found."))
    def test_get_repository_exception_raised(self, get_repo_mock):
        repository_name = 'user/repo'

        with self.assertRaisesRegex(Exception, "Repository not found."):
            self.gh_client.get_repository(repository_name)
