import django_filters
from .models import Meeting_app
import json


class Meeting_app_filter(django_filters.FilterSet):
    created_time = django_filters.CharFilter(method='filter_created_time')
    municipal_district = django_filters.CharFilter(method='filter_municipal_district')
    meeting_status = django_filters.CharFilter(method='filter_meeting_status')
    custom_data = django_filters.CharFilter(method='fiter_custom_data')
    order_by = django_filters.CharFilter(method='filter_order_by')
    multipurpose = django_filters.CharFilter(method='filter_multipurpose')

    class Meta:
        model = Meeting_app
        fields = ['id', 'created_time', 'status']

    def filter_created_time(self, queryset, name, value):
        date = value.split(',')
        return queryset.filter(created_time__range=date)

    def filter_meeting_status(self, queryset, name, value):
        status = value.split(',')
        return queryset.filter(status__id__in=status)

    def filter_municipal_district(self, queryset, name, value):
        district = value.split(',')
        return queryset.filter(municipal_district__id__in=district)

    def fiter_custom_data(self, queryset, name, value: dict):
        value = json.loads(value)
        filter = {}
        for key, value in value.items():
            filter[f"custom_data__{key}"] = value
        return queryset.filter(**filter)

    def filter_multipurpose(self, queryset, name, value):
        value = json.loads(value)
        filter = {}
        for key, value in value.items():
            filter[key] = value
        return queryset.filter(**filter)

    def filter_order_by(self, queryset, name, value):
        return queryset.order_by(value)
