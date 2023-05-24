from datetime import datetime
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

    @patch('integrations.github_api.GithubAPIClient.get_repository')
    def test_get_commits_from_repository(self, get_repository_mock):
        repository_name = 'user/repo'

        expected_commits = [MagicMock()] * 2

        repo_mock = get_repository_mock.return_value
        repo_mock.get_commits.return_value = expected_commits
        get_repository_mock.return_value = repo_mock

        commits = self.gh_client.get_commits_from_repository(repository_name)

        repo_mock.get_commits.assert_called_once()
        self.assertListEqual(commits, expected_commits)

    @patch('integrations.github_api.GithubAPIClient.get_repository')
    def test_get_commits_from_repository_since_date(self, get_repository_mock):
        repository_name = 'user/repo'
        since_date = datetime(2023, 1, 5)

        repo_mock = get_repository_mock.return_value

        self.gh_client.get_commits_from_repository(repository_name, since_date)

        repo_mock.get_commits.assert_called_once_with(since=since_date)
