from github.GithubException import UnknownObjectException
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from integrations.github_api import GithubAPIClient

from .models import Commit
from .serializers import CommitSerializer, RepositorySerializer


class CommitsView(ListModelMixin, GenericAPIView):
    """View for endpoints related to Commits."""
    queryset = Commit.objects.all()
    serializer_class = CommitSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """List all commits.

        :param request: Request object.
        :type request: Request
        :return: Response object containing serialized data for all commits.
        :rtype: Response
        """
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

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
