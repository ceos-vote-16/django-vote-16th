from django_filters import FilterSet, filters
from api.models import *


class UserFilter(FilterSet):
    part = filters.CharFilter(field_name='part', lookup_expr='icontains')
    team = filters.CharFilter(field_name='team', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['part', 'team']


class CandidateFilter(FilterSet):
    part = filters.CharFilter(field_name='part', lookup_expr='icontains')

    class Meta:
        model = Candidate
        fields = ['part']
