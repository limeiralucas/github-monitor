from datetime import datetime
from typing import Any, Optional

from github import Github
from github.Commit import Commit
from github.PaginatedList import PaginatedList
from github.Repository import Repository


class InvalidRequestUserException(Exception):
    """Represent an exception when a invalid user is provided to client creation."""
    def __init__(self) -> None:
        super().__init__("Request user is invalid or doesn't contain github credentials.")


class GithubAPIClient:
    """Class responsible for all actions related to Github."""
    def __init__(self, access_token: str) -> None:
        self.access_token = access_token
        self.client = Github(access_token)

    def get_repository(self, repo_fullname: str) -> Repository:
        """Fetch a repository from Github given a provided full name.

        :param repo_fullname: Repository full name (owner/repository_name)
        :type repo_fullname: str
        :raises UnknownObjectException: Raised if a repository with the given name is not found
        :raises BadCredentialsException: Raised if invalid credentials were provided to client
        :return: Repository object
        :rtype: Repository
        """

        return self.client.get_repo(repo_fullname)

    def get_commits_from_repository(
            self,
            repo_fullname: str,
            since: Optional[datetime] = None
    ) -> "PaginatedList[Commit]":
        """
        Fetch commits from a Github repository given a provided full name.
        A date can be provided to fetch commits between now and this date.

        :param repofull_name: Repository full name (owner/repository_name)
        :type repofull_name: str
        :param since: Date to fetch commits between it and now, defaults to None
        :type since: Optional[datetime], optional
        :raises BadCredentialsException: Raised if invalid credentials were provided to client
        :return: PaginatedList object (iterable) to access the commits from the repository
        :rtype: PaginatedList[Commit]
        """
        repo = self.get_repository(repo_fullname)

        args = {'since': since} if since else {}
        return repo.get_commits(**args)

    @classmethod
    def from_request_user(cls, request_user: Any) -> "GithubAPIClient":
        """Create a GithubAPIClient from a provided Django request user.

        :param request_user: Django request user
        :type request_user: Any
        :raises InvalidRequestUserException: User invalid/doesn't contain credentials
        :return: client created with the request user github access token
        :rtype: GithubAPIClient
        """
        try:
            social = request_user.social_auth.get(provider='github')
            access_token = social.extra_data['access_token']

            return cls(access_token)
        except Exception as e:
            raise InvalidRequestUserException() from e
