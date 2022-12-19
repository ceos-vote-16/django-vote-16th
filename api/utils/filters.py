from django_filters import FilterSet, filters
from api.models import *

class UserFilter(FilterSet):
    # 파트별 조회 필요
    class Meta:
        model = User
        fields = []