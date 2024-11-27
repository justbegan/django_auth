import django_filters
import json
from django.db.models import Q

from apps.news.models import News
from services.current import get_current_section


class News_filter(django_filters.FilterSet):
    json_search = django_filters.CharFilter(method='json_search_method')
    search = django_filters.CharFilter(method='filter_search')
    created_at = django_filters.CharFilter(method='filter_created_at')
    get_all = django_filters.CharFilter(method='filter_get_all')

    class Meta:
        model = News
        fields = ['title', 'text']

    def json_search_method(self, queryset, name, value):
        data = json.loads(value)
        return queryset.filter(**data)

    def filter_created_at(self, queryset, name, value):
        date = value.split(',')
        return queryset.filter(created_at__range=date)

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            (
                Q(title__icontains=value)
                | Q(text__icontains=value)
            )
        )

    def filter_get_all(self, queryset, name, value):
        if value == 0:
            return queryset.filter(section=get_current_section(self.request))
        else:
            return queryset
