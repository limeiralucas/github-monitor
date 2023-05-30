from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

from integrations.github_api import (GithubAPIClient,
                                     InvalidRequestUserException)


class TestGithubAPIClient(TestCase):
    def setUp(self) -> None:
        self.access_token = 'access-token'
        self.gh_client = GithubAPIClient(self.access_token)

    @patch('integrations.github_api.Github')
    def test_client_initialization(self, github_client_mock):
        """Check if client is initialized with provided access token."""
        access_token = 'token'
        client = GithubAPIClient(access_token)

        assert client
        github_client_mock.assert_called_once_with(access_token)

    @patch('integrations.github_api.Github')
    def test_from_request_user(self, github_client_mock):
        """Check if client is initialized with provided request user."""
        access_token = 'token'

        request_user = MagicMock()
        social_mock = request_user.social_auth.get.return_value
        social_mock.extra_data = {"access_token": access_token}
        request_user.social_auth.get_return_value = social_mock

        client = GithubAPIClient.from_request_user(request_user)

        assert client
        github_client_mock.assert_called_once_with(access_token)
        request_user.social_auth.get.assert_called_once_with(provider="github")

    def test_from_invalid_request_user(self):
        """Check if InvalidRequestUserException is raised if a invalid request user is provided."""
        request_user = MagicMock()
        request_user.social_auth.get = MagicMock(side_effect=Exception())

        with self.assertRaisesRegex(
            InvalidRequestUserException,
            "Request user is invalid or doesn't contain github credentials."
        ):
            GithubAPIClient.from_request_user(request_user)

    @patch('github.Github.get_repo')
    def test_get_repository(self, get_repo_mock):
        """Check if a repository is fetched given a provided full name.

        Check if github client get_repo method is called with repository name.
        Check if the repository object from github client is returned.
        """
        repository_name = 'user/repo'

        repo_mock = MagicMock()
        repo_mock.name = repository_name
        get_repo_mock.return_value = repo_mock

        repo = self.gh_client.get_repository(repository_name)

        get_repo_mock.assert_called_once_with(repository_name)
        assert repo == repo_mock

    @patch('github.Github.get_repo', side_effect=Exception("Repository not found."))
    def test_get_repository_exception_raised(self, get_repo_mock):
        """Check if exception is raised in case of a problem when fetching the repository.

        Check if get_repository raises a exception when a exception is raised by github client lib.
        """
        repository_name = 'user/repo'

        with self.assertRaisesRegex(Exception, "Repository not found."):
            self.gh_client.get_repository(repository_name)

    @patch('integrations.github_api.GithubAPIClient.get_repository')
    def test_get_commits_from_repository(self, get_repository_mock):
        """Check commits from a repository are fetched given a provided repository full name.

        Check if get_commits method from the repository object is called.
        Check if a iterable is returned contained the requested commits.
        """
        repository_name = 'user/repo'

        expected_commits = [MagicMock()] * 2

        repo_mock = get_repository_mock.return_value
        repo_mock.get_commits.return_value = expected_commits
        get_repository_mock.return_value = repo_mock

        commits = self.gh_client.get_commits_from_repository(repository_name)

        repo_mock.get_commits.assert_called_once()
        self.assertCountEqual(commits, expected_commits)

    @patch('integrations.github_api.GithubAPIClient.get_repository')
    def test_get_commits_from_repository_since_date(self, get_repository_mock):
        """Check commits from a repository are fetched for a specific time window.

        Check if repository object get_commits method is called with provided since param.
        """
        repository_name = 'user/repo'
        since_date = datetime(2023, 1, 5)

        repo_mock = get_repository_mock.return_value

        self.gh_client.get_commits_from_repository(repository_name, since_date)

        repo_mock.get_commits.assert_called_once_with(since=since_date)
