from django_filters import rest_framework as filters
from github.GithubException import UnknownObjectException
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from integrations.github_api import GithubAPIClient

from .filters import CommitFilter
from .models import Commit, Repository
from .serializers import CommitSerializer, RepositorySerializer
from .tasks import get_last_30_days_repo_commits


class CustomPagination(PageNumberPagination):
    """Custom pagination class to include total number of pages."""
    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data["total_pages"] = self.page.paginator.num_pages
        response.data["page"] = self.page.number

        return response


class CommitsView(ListAPIView):
    """View for endpoints related to Commits."""
    queryset = Commit.objects.all()
    serializer_class = CommitSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filter_backs = (filters.DjangoFilterBackend,)
    filterset_class = CommitFilter

    def get(self, request: Request, *args, **kwargs) -> Response:
        """List all commits.

        :param request: Request object.
        :type request: Request
        :return: Response object containing serialized data for all commits.
        :rtype: Response
        """
        return self.list(request, *args, **kwargs)


class RepositoriesView(GenericAPIView):
    """View for endpoints related to Repositories."""
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """Create a repository using provided data.

        Also, create a async task to fetch the last 30 days commits from this repository.

        :param request: Request object.
        :type request: Request
        :return: Response object containg serialized data of created repository.
        :rtype: Response
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        repo_fullname = serializer.validated_data['name']

        try:
            gh_client = GithubAPIClient.from_request_user(request.user)
            gh_client.get_repository(repo_fullname)
        except UnknownObjectException:
            return Response(status=status.HTTP_404_NOT_FOUND)

        repository = serializer.save()

        get_last_30_days_repo_commits.delay(gh_client.access_token, repository.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
