import django_filters

from .models import Profiles_manager_app
from apps.constructor.filter import Base_filter


class Profiles_manager_app_filter(Base_filter):
    id = django_filters.CharFilter(method='filter_id')
    status = django_filters.CharFilter(method='filter_status')
    author = django_filters.CharFilter(method='filter_author')

    class Meta:
        model = Profiles_manager_app
        fields = ['id']

    def filter_id(self, queryset, name, value):
        return queryset.filter(id=value)

    def filter_status(self, queryset, name, value):
        ids = [int(id) for id in value.split(',')]
        return queryset.filter(status__in=ids)

    def filter_author(self, queryset, name, value):
        ids = value.split(',')
        return queryset.filter(author__id__in=ids)
