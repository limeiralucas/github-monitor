from github.GithubException import UnknownObjectException
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from integrations.github_api import GithubAPIClient

from .models import Commit
from .serializers import CommitSerializer, RepositorySerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def commit_list_view(request):
    commits = Commit.objects.all()
    serializer = CommitSerializer(commits, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def repository_create_view(request):
    serializer = RepositorySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        gh_client = GithubAPIClient.from_request_user(request.user)
        gh_client.get_repository(serializer.validated_data['name'])
    except UnknownObjectException:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
