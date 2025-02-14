import django_filters
from django.db.models import Q

from .models import Profile
from apps.constructor.filter import Base_filter


class Profile_filter(Base_filter):
    municipal_district = django_filters.CharFilter(method='filter_municipal_district')
    all_field = django_filters.CharFilter(method='search_all_field')
    roles = django_filters.CharFilter(method='filter_roles')

    class Meta:
        model = Profile
        fields = ['municipal_district']

    def filter_municipal_district(self, queryset, name, value):
        district = value.split(',')
        return queryset.filter(municipal_district__id__in=district)

    def filter_roles(self, queryset, name, value):
        roles = value.split(',')
        return queryset.filter(role__id__in=roles)

    def search_all_field(self, queryset, name, value):
        q = queryset.filter(
            (
                Q(title__icontains=value)
                | Q(municipal_district__RegionNameE__icontains=value)
                | Q(settlement__MunicNameE__icontains=value)
                | Q(locality__LocNameE__icontains=value)
                | Q(section__title__icontains=value)
                | Q(profile_type__title__icontains=value)
            )
        )
        return q
