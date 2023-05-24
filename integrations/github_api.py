from github import Github
from github.Repository import Repository


class GithubAPIClient:
    """Class responsible to all actions related to Github."""
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
