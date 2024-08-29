import django_filters
from ..models import Application
import json


class Application_filter(django_filters.FilterSet):
    id = django_filters.CharFilter(method='filter_id')
    created_time = django_filters.CharFilter(method='filter_created_time')
    status = django_filters.CharFilter(method='filter_status')
    custom_data = django_filters.CharFilter(method='fiter_custom_data')
    order_by = django_filters.CharFilter(method='filter_order_by')

    class Meta:
        model = Application
        fields = ['id', 'created_time', 'status']

    def filter_id(self, queryset, name, value):
        print(name)
        return queryset.filter(id=value)

    def filter_created_time(self, queryset, name, value):
        date = value.split(',')
        return queryset.filter(created_time__range=date)

    def filter_status(self, queryset, name, value):
        status = value.split(',')
        return queryset.filter(status__title__in=status)

    def fiter_custom_data(self, queryset, name, value: dict):
        value = json.loads(value)
        filter = {}
        for key, value in value.items():
            filter[f"custom_data__{key}"] = value
        return queryset.filter(**filter)

    def filter_order_by(self, queryset, name, value):
        return queryset.order_by(value)
