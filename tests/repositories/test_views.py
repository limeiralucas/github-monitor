import json
from datetime import datetime, timedelta
from typing import List
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from github.GithubException import UnknownObjectException

from repositories.models import Commit, Repository
from repositories.serializers import CommitSerializer, RepositorySerializer


class TestCommitsView(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='test_user', password='test')
        self.repository = Repository.objects.create(name='Test Repository')
        self.commits = self.create_random_commits(number_commits=20, repository=self.repository)

    @staticmethod
    def create_random_commits(number_commits: int, repository: Repository) -> List[Commit]:
        return [
            Commit.objects.create(
                message=f'Commit {i}',
                sha=f'12345{i}',
                author=f'Jane Smith {i}',
                url=f'https://github.com/user/repo/commits/12345{i}',
                date=datetime.now() + timedelta(days=i),
                avatar=f'https://example.com/avatar{i}.jpg',
                repository=repository
            ) for i in range(number_commits)
        ]

    def test_commits_list_unauthenticated(self):
        """Check if authentication is required to fetch commits."""
        response = self.client.get('/api/commits', follow=True)

        self.assertEqual(response.status_code, 403)

    def test_commits_list(self):
        """Check if the requested commits are returned."""
        self.client.force_login(self.user)
        response = self.client.get('/api/commits', follow=True)

        commits = Commit.objects.all()[:10]
        serializer = CommitSerializer(commits, many=True)

        response_commits = response.data["results"]

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response_commits, serializer.data)
        self.assertEqual(response.data["count"], 20)
        self.assertIsNotNone(response.data["next"])
        self.assertIsNone(response.data["previous"])

    def test_commits_list_pagination(self):
        """Check if the requested commits are returned with pagination."""
        # Check first page
        self.client.force_login(self.user)
        response = self.client.get('/api/commits', follow=True)

        all_commits = Commit.objects.all()
        first_10_commits = all_commits[:10]
        serializer = CommitSerializer(first_10_commits, many=True)

        response_commits = response.data["results"]

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response_commits, serializer.data)
        self.assertEqual(response.data["count"], 20)

        # Should have a next page, but not a previous
        self.assertIsNotNone(response.data["next"])
        self.assertIsNone(response.data["previous"])

        # Check second page
        response = self.client.get('/api/commits?page=2', follow=True)

        last_10_commits = all_commits[10:]
        serializer = CommitSerializer(last_10_commits, many=True)

        response_commits = response.data["results"]

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response_commits, serializer.data)
        self.assertEqual(response.data["count"], 20)

        # Should have a prevous page, but not a next
        self.assertIsNone(response.data["next"])
        self.assertIsNotNone(response.data["previous"])

    def tearDown(self):
        for commit in self.commits:
            commit.delete()

        self.repository.delete()
        self.user.delete()


class TestRepositoriesView(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='test_user', password='test')

    def test_repository_create_unauthenticated(self):
        """Check if authentication is required to add repository."""
        response = self.client.post('/api/repositories', follow=True)

        self.assertEqual(response.status_code, 403)

    @patch('repositories.tasks.get_last_30_days_repo_commits.delay')
    @patch('integrations.github_api.GithubAPIClient.from_request_user')
    def test_repository_create(self, from_request_user_mock, get_commits_task_mock):
        """Check if repository is created and celery task to fetch commits is setup."""
        access_token = 'access-token'
        repository_fullname = 'user/repo'
        gh_client_mock = from_request_user_mock.return_value
        gh_client_mock.access_token = access_token

        self.client.force_login(self.user)
        response = self.client.post(
            '/api/repositories/',
            json.dumps({'name': repository_fullname}),
            content_type='application/json',
            follow=True
        )

        repository = Repository.objects.first()
        serializer = RepositorySerializer(repository)

        gh_client_mock.get_repository.assert_called_once_with(repository_fullname)
        get_commits_task_mock.assert_called_once_with(access_token, repository.id)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, serializer.data)

    def test_repository_create_invalid_data(self):
        """Check if it returns 400 when invalid data is sent."""
        self.client.force_login(self.user)
        response = self.client.post(
            '/api/repositories/',
            json.dumps({}),
            content_type='application/json',
            follow=True
        )

        self.assertEqual(response.status_code, 400)

    @patch('integrations.github_api.GithubAPIClient.from_request_user')
    def test_repository_create_not_found(self, from_request_user_mock):
        """Check if it returns 404 when the repository is not found on Github"""
        gh_client_mock = from_request_user_mock.return_value
        gh_client_mock.get_repository.side_effect = UnknownObjectException(None, None, None)
        from_request_user_mock.return_value = gh_client_mock

        self.client.force_login(self.user)
        response = self.client.post(
            '/api/repositories/',
            json.dumps({'name': 'user/invalid-repo'}),
            content_type='application/json',
            follow=True
        )

        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        self.user.delete()
