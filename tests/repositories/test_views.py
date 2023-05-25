from django.contrib.auth.models import User
from django.test import TestCase

from repositories.models import Commit, Repository
from repositories.serializers import CommitSerializer


class TestCalls(TestCase):
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
