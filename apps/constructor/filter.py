import django_filters
import json
from django.db.models import Q

from .models import Application


class Base_filter(django_filters.FilterSet):
    json_search = django_filters.CharFilter(method='json_search_method')

    class Meta:
        abstract = True

    def json_search_method(self, queryset, name, value):
        data = json.loads(value)
        return queryset.filter(**data)


class Base_application_filter(Base_filter):
    id = django_filters.CharFilter(method='filter_id')
    created_at = django_filters.CharFilter(method='filter_created_at')
    municipal_district = django_filters.CharFilter(method='filter_municipal_district')
    status = django_filters.CharFilter(method='filter_status')
    contest = django_filters.CharFilter(method='filter_contest')
    year = django_filters.CharFilter(method='filter_year')
    custom_data = django_filters.CharFilter(method='fiter_custom_data')
    order_by = django_filters.CharFilter(method='filter_order_by')
    multipurpose = django_filters.CharFilter(method='filter_multipurpose')
    all_field = django_filters.CharFilter(method='search_all_field')
    profile_type = django_filters.CharFilter(method='filter_profile_type')

    class Meta:
        abstract = True

    def filter_id(self, queryset, name, value):
        return queryset.filter(id=value)

    def filter_created_at(self, queryset, name, value):
        date = value.split(',')
        return queryset.filter(created_at__range=date)

    def filter_status(self, queryset, name, value):
        status = value.split(',')
        return queryset.filter(status__title__in=status)

    def filter_contest(self, queryset, name, value):
        contest = value.split(',')
        return queryset.filter(contest__id__in=contest)

    def filter_municipal_district(self, queryset, name, value):
        district = value.split(',')
        return queryset.filter(municipal_district__RegionNameE__in=district)

    def filter_year(self, queryset, name, value):
        return queryset.filter(contest__year=value)

    def fiter_custom_data(self, queryset, name, value: dict):
        """
        {"smi_used": 2}
        """
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
        order_by_mapping = {
            "profile_type": "author__profile_type__title",
            "-profile_type": "-author__profile_type__title"
        }
        value = order_by_mapping[value] if order_by_mapping.get(value, None) else value
        return queryset.order_by(value)

    def search_all_field(self, queryset, name, value):
        q1 = queryset.filter(
            (
                Q(title__icontains=value)
                | Q(municipal_district__RegionNameE__icontains=value)
                | Q(settlement__MunicNameE__icontains=value)
                | Q(locality__LocNameE__icontains=value))
        )
        q2 = queryset.filter(custom_data__icontains=value)
        combined_queryset = q1.union(q2)
        return combined_queryset

    def filter_profile_type(self, queryset, name, value):
        profile_types = value.split(',')
        return queryset.filter(author__profile_type__title__in=profile_types)


class Application_filter(Base_application_filter):
    project_type = django_filters.CharFilter(method='filter_project_type')

    class Meta:
        model = Application
        fields = ['id', 'created_at', 'status']

    def filter_project_type(self, queryset, name, value):
        project_type = value.split(',')
        return queryset.filter(project_type__title__in=project_type)

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


class Application_map_filter(django_filters.FilterSet):

    municipal_district = django_filters.CharFilter(method='filter_municipal_district')
    all_field = django_filters.CharFilter(method='search_all_field')
    contest = django_filters.CharFilter(method='filter_contest')

    class Meta:
        model = Application
        fields = ['municipal_district', 'project_type']

    def filter_municipal_district(self, queryset, name, value):
        district = value.split(',')
        return queryset.filter(municipal_district__id__in=district)

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

    def filter_contest(self, queryset, name, value):
        contests = value.split(',')
        return queryset.filter(contest__id__in=contests)
