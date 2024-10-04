import django_filters
from apps.constructor.models import Application


class Application_rating_filter(django_filters.FilterSet):
    contest = django_filters.filters.CharFilter(method='filter_contest')
    municipal_district = django_filters.CharFilter(method='filter_municipal_district')
    project_type = django_filters.CharFilter(method='filter_project_type')
    status = django_filters.filters.CharFilter(method='filter_status')

    class Meta:
        model = Application
        fields = ['contest', 'municipal_district']

    def filter_contest(self, queryset, name, value):
        contest = value.split(',')
        return queryset.filter(contest__id__in=contest)

    def filter_municipal_district(self, queryset, name, value):
        district = value.split(',')
        return queryset.filter(municipal_district__id__in=district)

    def filter_project_type(self, queryset, name, value):
        project_type = value.split(',')
        return queryset.filter(project_type__id__in=project_type)

    def filter_status(self, queryset, name, value):
        application_status = value.split(',')
        return queryset.filter(status__id__in=application_status)
