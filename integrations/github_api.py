from github import Github
from github.GithubException import UnknownObjectException
from github.Repository import Repository


class RepositoryNotFoundException(Exception):
    def __init__(self, original_exc: Exception) -> None:
        """Represent exception when a repository is not found on Github.

        :param original_exc: Original exception from github library
        :type original_exc: Exception
        """
        super().__init__()
        self.original_exc = original_exc


class GithubAPIClient:
    """Class responsible to all actions related to Github."""
    def __init__(self, access_token: str) -> None:
        self.client = Github(access_token)

    def get_repository(self, repo_full_name: str) -> Repository:
        """Fetch a repository from Github given a provided full name.

        :param repo_full_name: Repository full name (owner/repository_name)
        :type repo_full_name: str
        :raises RepositoryNotFoundException: Raised if a repository with the given name is not found
        :return: Repository object
        :rtype: Repository
        """
        try:
            return self.client.get_repo(repo_full_name)
        except UnknownObjectException as e:
            raise RepositoryNotFoundException(e) from e
