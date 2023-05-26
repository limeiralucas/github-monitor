import logging
from datetime import datetime, timedelta, timezone

from celery import shared_task
from django.db import transaction

from githubmonitor.celery import app  # noqa: F401
from integrations.github_api import GithubAPIClient
from repositories.adapters import CommitAdapter
from repositories.models import Repository
from repositories.serializers import CommitSerializer


@shared_task
def get_last_30_days_repo_commits(github_access_token: str, repository_id: int):
    """Fetch last 30 days commits of a repository and save them to database.

    :param github_access_token: Github access token.
    :type github_access_token: str
    :param repository_id: Repository id (pk) from database.
    :type repository_id: int
    """
    gh_client = GithubAPIClient(github_access_token)
    last_thirty_days = datetime.now(tz=timezone.utc) - timedelta(days=30)

    repository = Repository.objects.get(pk=repository_id)

    commits = gh_client.get_commits_from_repository(repository.name, since=last_thirty_days)

    commits_data_list = [CommitAdapter.from_data(commit.raw_data) for commit in commits]
    logging.info("Retrieved %s commits from Github.", len(commits_data_list))

    with transaction.atomic():
        for commit_data in commits_data_list:
            serializer = CommitSerializer(data=commit_data)
            serializer.is_valid(raise_exception=True)

            serializer.validated_data['repository'] = repository
            serializer.save()
