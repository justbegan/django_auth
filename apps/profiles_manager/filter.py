import django_filters

from .models import Profiles_manager_app


class Profiles_manager_app_filter(django_filters.FilterSet):
    id = django_filters.CharFilter(method='filter_id')

    class Meta:
        model = Profiles_manager_app
        fields = ['id']

    def filter_id(self, queryset, name, value):
        return queryset.filter(id=value)
