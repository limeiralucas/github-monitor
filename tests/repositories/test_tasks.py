from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from django.test import TestCase
from freezegun import freeze_time

from repositories.adapters import CommitAdapter
from repositories.models import Commit, Repository
from repositories.tasks import get_last_30_days_repo_commits


class TestTasks(TestCase):
    def setUp(self) -> None:
        self.repository = Repository.objects.create(name="Test Repository")
        self.commits_from_api = [
            {
                "commit": {
                    "message": "commit 01",
                    "author": {
                        "name": "John Doe",
                        "date": "2023-04-14T16:00:49Z",
                    },
                },
                "author": {
                    "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                },
                "url": "https://api.github.com/repos/user/repo/commits/12345",
                "sha": "12345",
            },
            {
                "commit": {
                    "message": "commit 02",
                    "author": {
                        "name": "Jane Green",
                        "date": "2023-04-16T12:00:49Z",
                    },
                },
                "author": {
                    "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                },
                "url": "https://api.github.com/repos/user/repo/commits/67890",
                "sha": "67890",
            },
        ]


    @freeze_time("2023-04-01 12:00:00")
    @patch('repositories.tasks.GithubAPIClient')
    def test_get_last_30_days_repo_commits(self, gh_client_mock):
        """Check if commits are fetched using GithubAPIClient and if they are saved on db."""
        access_token = "access-token"
        last_thirty_days = datetime.now(tz=timezone.utc) - timedelta(days=30)

        gh_client_mock.return_value.get_commits_from_repository.return_value = [
            MagicMock(raw_data=data) for data in self.commits_from_api
        ]

        get_last_30_days_repo_commits(access_token, self.repository.id)
        saved_commits = Commit.objects.all().order_by("sha")

        # Check if GithubAPIClient methods were called as expected
        gh_client_mock.assert_called_once_with(access_token)
        gh_client_mock.return_value.get_commits_from_repository.assert_called_once_with(
            self.repository.name, since=last_thirty_days
        )

        # Use serializer and compare saved commits with commits returned by Github api
        expected_commits = sorted([CommitAdapter.from_data(data) for data in self.commits_from_api], key=lambda c: c["sha"])

        for commit, commit_data in zip(saved_commits, expected_commits):
            self.assertEqual(commit.message, commit_data['message'])
            self.assertEqual(commit.sha, commit_data['sha'])
            self.assertEqual(commit.author, commit_data['author'])
            self.assertEqual(commit.url, commit_data['url'])
            self.assertEqual(commit.avatar, commit_data['avatar'])
            self.assertEqual(commit.repository, self.repository)
