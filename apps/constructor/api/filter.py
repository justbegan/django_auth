import django_filters
import json
from django.db.models import Q

from ..models import Application


class Application_filter(django_filters.FilterSet):
    id = django_filters.CharFilter(method='filter_id')
    created_time = django_filters.CharFilter(method='filter_created_time')
    municipal_district = django_filters.CharFilter(method='filter_municipal_district')
    project_type = django_filters.CharFilter(method='filter_project_type')
    status = django_filters.CharFilter(method='filter_status')
    custom_data = django_filters.CharFilter(method='fiter_custom_data')
    order_by = django_filters.CharFilter(method='filter_order_by')
    multipurpose = django_filters.CharFilter(method='filter_multipurpose')
    all_field = django_filters.CharFilter(method='search_all_field')

    class Meta:
        model = Application
        fields = ['id', 'created_time', 'status']

    def filter_id(self, queryset, name, value):
        return queryset.filter(id=value)

    def filter_created_time(self, queryset, name, value):
        date = value.split(',')
        return queryset.filter(created_time__range=date)

    def filter_status(self, queryset, name, value):
        status = value.split(',')
        return queryset.filter(status__id__in=status)

    def filter_municipal_district(self, queryset, name, value):
        district = value.split(',')
        return queryset.filter(municipal_district__id__in=district)

    def filter_project_type(self, queryset, name, value):
        project_type = value.split(',')
        return queryset.filter(project_type__id__in=project_type)

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

    def search_all_field(self, queryset, name, value):
        q1 = queryset.filter(
            (
                Q(title__icontains=value)
                | Q(municipal_district__RegionNameE__icontains=value)
                | Q(settlement__MunicNameE__icontains=value)
                | Q(locality__LocNameE__icontains=value)
                | Q(project_type__title__icontains=value))
        )
        q2 = queryset.filter(custom_data__icontains=value)
        combined_queryset = q1.union(q2)
        return combined_queryset
