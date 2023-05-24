from datetime import datetime
from typing import Optional

from github import Github
from github.Commit import Commit
from github.PaginatedList import PaginatedList
from github.Repository import Repository


class GithubAPIClient:
    """Class responsible for all actions related to Github."""
    def __init__(self, access_token: str) -> None:
        self.client = Github(access_token)

    def get_repository(self, repo_full_name: str) -> Repository:
        """Fetch a repository from Github given a provided full name.

        :param repo_full_name: Repository full name (owner/repository_name)
        :type repo_full_name: str
        :raises UnknownObjectException: Raised if a repository with the given name is not found
        :raises BadCredentialsException: Raised if invalid credentials were provided to client
        :return: Repository object
        :rtype: Repository
        """

        return self.client.get_repo(repo_full_name)

    def get_commits_from_repository(
            self,
            repo_full_name: str,
            since: Optional[datetime] = None
    ) -> "PaginatedList[Commit]":
        """
        Fetch commits from a Github repository given a provided full name.
        A date can be provided to fetch commits between now and this date.

        :param repo_full_name: Repository full name (owner/repository_name)
        :type repo_full_name: str
        :param since: Date to fetch commits between it and now, defaults to None
        :type since: Optional[datetime], optional
        :return: PaginatedList object (iterable) to access the commits from the repository
        :rtype: PaginatedList[Commit]
        """
        repo = self.get_repository(repo_full_name)

        return repo.get_commits(since=since)
