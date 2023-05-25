from datetime import datetime, timedelta, timezone

from celery import shared_task

from githubmonitor.celery import app  # noqa: F401
from integrations.github_api import GithubAPIClient
from repositories.adapters import CommitAdapter
from repositories.serializers import CommitSerializer


@shared_task
def get_last_thirty_days_repo_commits(github_access_token: str, repository_fullname: str):
    gh_client = GithubAPIClient(github_access_token)
    last_thirty_days = datetime.now(tz=timezone.utc) - timedelta(days=30)

    commits = gh_client.get_commits_from_repository(repository_fullname, since=last_thirty_days)

    all_commits = [CommitAdapter.from_data(commit.raw_data) for commit in commits]
    serializer = CommitSerializer(data=all_commits, many=True)

    serializer.is_valid(raise_exception=True)

    print(f"Fetched {len(all_commits)}")
