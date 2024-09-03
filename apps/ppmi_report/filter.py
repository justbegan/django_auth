import django_filters
from apps.constructor.models import Application


class Application_rating_filter(django_filters.FilterSet):
    contest = django_filters.filters.CharFilter(method='filter_contest')
    municipal_district = django_filters.CharFilter(method='filter_municipal_district')

    class Meta:
        model = Application
        fields = ['contest', 'municipal_district']

    def filter_contest(self, queryset, name, value):
        contest = value.split(',')
        return queryset.filter(contest__id__in=contest)

    def filter_municipal_district(self, queryset, name, value):
        district = value.split(',')
        return queryset.filter(municipal_district__id__in=district)
