import django_filters

from .models import CustomUser


class Custom_user_filter(django_filters.FilterSet):
    id = django_filters.CharFilter(method='filter_id')
    is_active = django_filters.NumberFilter(
        method='filter_is_active',
        label="Фильтрация по статусу активности (2 = все, 1 = активен, 0 = неактивен)",
    )
    role = django_filters.CharFilter(method='filter_role')
    section = django_filters.CharFilter(method='filter_section')
    municipal_district = django_filters.CharFilter(method='filter_municipal_district')
    settlement = django_filters.CharFilter(method='filter_settlement')
    locality = django_filters.CharFilter(method='filter_locality')

    class Meta:
        model = CustomUser
        fields = ['id', 'is_active']

    def filter_id(self, queryset, name, value):
        return queryset.filter(id=value)

    def filter_is_active(self, queryset, name, value: str):
        value = int(value)
        if value == 0:
            return queryset.filter(is_active=False)
        elif value == 1:
            return queryset.filter(is_active=True)
        else:
            return queryset

    def filter_role(self, queryset, name, value: str):
        return queryset.filter(profile__role__id=value)

    def filter_section(self, queryset, name, value: str):
        return queryset.filter(profile__section__id=value)

    def filter_municipal_district(self, queryset, name, value: str):
        return queryset.filter(profile__municipal_district__id=value)

    def filter_settlement(self, queryset, name, value: str):
        return queryset.filter(profile__settlement__id=value)

    def filter_locality(self, queryset, name, value: str):
        return queryset.filter(profile__locality__id=value)
