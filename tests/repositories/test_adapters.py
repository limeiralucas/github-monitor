from django.test import TestCase

from repositories.adapters import CommitAdapter


class CommitAdapterTest(TestCase):
    def test_from_data(self):
        data = [
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

        expected_results = [
            {
                "message": "commit 01",
                "sha": "12345",
                "author": "John Doe",
                "url": "https://api.github.com/repos/user/repo/commits/12345",
                "date": "2023-04-14T16:00:49Z",
                "avatar": "https://github.com/images/error/octocat_happy.gif",
            },
            {
                "message": "commit 02",
                "sha": "67890",
                "author": "Jane Green",
                "url": "https://api.github.com/repos/user/repo/commits/67890",
                "date": "2023-04-16T12:00:49Z",
                "avatar": "https://github.com/images/error/octocat_happy.gif",
            },
        ]

        results = [CommitAdapter.from_data(commit_data) for commit_data in data]
        self.assertCountEqual(results, expected_results)
