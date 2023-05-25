import json

from django.contrib.auth.models import User
from django.test import TestCase

from repositories.models import Commit, Repository
from repositories.serializers import CommitSerializer, RepositorySerializer


class TestCommitsView(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='test_user', password='test')
        self.repository = Repository.objects.create(name='Test Repository')
        self.commits = [
            Commit.objects.create(
                message='Commit 1',
                sha='123456',
                author='John Doe',
                url='https://github.com/user/repo/commits/123456',
                date='2023-05-01T10:00:00Z',
                avatar='https://example.com/avatar.jpg',
                repository=self.repository
            ),
            Commit.objects.create(
                message='Commit 2',
                sha='789012',
                author='Jane Smith',
                url='https://github.com/user/repo/commits/789012',
                date='2023-05-02T11:00:00Z',
                avatar='https://example.com/avatar.jpg',
                repository=self.repository
            )
        ]

    def test_commits_list_unauthenticated(self):
        """Check if authentication is required to fetch commits."""
        response = self.client.get('/api/commits', follow=True)

        self.assertEqual(response.status_code, 403)

    def test_commits_list(self):
        """Check if the requested commits are returned."""
        self.client.force_login(self.user)
        response = self.client.get('/api/commits', follow=True)

        commits = Commit.objects.all()
        serializer = CommitSerializer(commits, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

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

    def test_repository_create(self):
        """Check if repository is created."""
        self.client.force_login(self.user)
        response = self.client.post(
            '/api/repositories/',
            json.dumps({'name': 'user/repo'}),
            content_type='application/json',
            follow=True
        )

        repository = Repository.objects.first()
        serializer = RepositorySerializer(repository)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, serializer.data)

    def test_repository_create_invalid_data(self):
        """Check if repository returns 400 when invalid data is sent."""
        self.client.force_login(self.user)
        response = self.client.post(
            '/api/repositories/',
            json.dumps({}),
            content_type='application/json',
            follow=True
        )

        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        self.user.delete()
