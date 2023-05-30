from django_filters import rest_framework as filters

from .models import Commit


class CommitFilter(filters.FilterSet):
    author = filters.CharFilter(field_name='author', lookup_expr='iexact')
    repository = filters.CharFilter(field_name='repository__name', lookup_expr='iexact')

    class Meta:
        model = Commit
        fields = ('author', 'repository')
