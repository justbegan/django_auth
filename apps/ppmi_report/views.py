from rest_framework.views import APIView, Response, Request
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.constructor.models import Application
from .serializers import (Application_registry_serializer, Results_of_applications_acceptance_serializer,
                          Application_rating_serializer, Application_stat_by_district_serializer)
from apps.constructor.services.current import get_current_section
from .filter import Application_rating_filter
from apps.locations.models import Municipal_district, Settlement


class Application_registry(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        obj = Application.objects.filter(section=get_current_section(request))
        ser = Application_registry_serializer(obj, many=True)
        result = {
            "fields_description": {
                'municipal_district': 'Район',
                'settlement': 'Поселение',
                'locality': 'Населенный пункт',
                'title': 'Название проекта',
                'project_type': 'Типология проекта',
                'total_price': 'Стоимость проекта'
            },
            "data": ser.data
        }
        return Response(result)


class Results_of_applications_acceptance(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        obj = Application.objects.filter(section=get_current_section(request))
        ser = Results_of_applications_acceptance_serializer(obj, many=True)
        result = {
            "fields_description": {
                'municipal_district': 'Район',
                'settlement': 'Поселение',
                'locality': 'Населенный пункт',
                'title': 'Название проекта',
                'project_type': 'Типология проекта',
                'total_price': 'Стоимость проекта',
                'get_financing_settlement_budget': 'Вклад поселения',
                'get_financing_people': 'Вклад населения',
                'get_financing_sponsors': 'Вклад спонсоров',
                'get_financing_republic_grant': 'Сумма субсидии'
            },
            "data": ser.data
        }
        return Response(result)


class Application_rating(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = Application_rating_serializer
    queryset = Application.objects.all().order_by('-id')
    filter_backends = [DjangoFilterBackend]
    filterset_class = Application_rating_filter

    def get_queryset(self):
        queryset = super().get_queryset()
        obj = queryset.filter(author=self.request.user.id)
        return obj

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        custom_data = {
            'fields_description': {
                'municipal_district': 'Район',
                'settlement': 'Поселение',
                'locality': 'Населенный пункт',
                'title': 'Название проекта',
                'rating': 'Рейтинг',
                'get_financing_republic_grant': 'Сумма субсидии',
                'total_point': 'Итог. балл'
            },
            'data': self.custom_method(response.data),
        }
        return Response(custom_data)

    def custom_method(self, data):
        sorted_data = sorted(data, key=lambda x: (x['created_at'], -x['total_point']))
        for num, i in enumerate(sorted_data, start=1):
            i['rating'] = num
        return sorted_data


class Application_stat_by_district(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('status', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter('contest', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter('contest__year', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False)
        ]
    )
    def get(self, request: Request):
        filter = {
            'section__id': get_current_section(request).id
        }
        for key, value in request.query_params.items():
            filter[key] = value
        result = {
            'fields_description': {
                'municipal_district': 'Район',
                'settlement_count': 'Число поселений',
                'application_count': 'Число заявок',
                "settlement_app_percent": 'Поселен. с заявками',
                "application_winner_count": 'Победителей',
                "application_winner_percent": 'Доля победителей',
                "application_financing_settlement_budget": 'Местный бюджет',
                "application_financing_people": 'Население',
                "application_financing_sponsors": 'Спонсоры',
                "application_financing_republic_grant": 'Субсидия',
                "application_finded_sum_percent": 'Доля привл. средств',
            },
            'data': []
        }
        settlement_obj = Settlement.objects
        application_obj = Application.objects.filter(**filter)
        d = []
        for municipal_district in Municipal_district.objects.all():
            app_by_md = application_obj.filter(municipal_district=municipal_district)
            settlement_count = settlement_obj.filter(RegID=municipal_district).count()
            application_count = application_obj.filter(municipal_district=municipal_district).count()
            application_winner_count = application_obj.filter(
                municipal_district=municipal_district, status__title="Победила").count()
            application_winner_percent = self.get_percentage(application_winner_count, application_count)
            application_financing_settlement_budget = self.get_financing_settlement_budget(
                app_by_md
            )
            application_financing_people = self.get_financing_people(app_by_md)
            application_financing_sponsors = self.get_financing_sponsors(app_by_md)
            application_financing_republic_grant = self.get_financing_republic_grant(app_by_md)
            application_finded_sum_percent = self.get_percentage(
                sum([application_financing_settlement_budget,
                     application_financing_people,
                     application_financing_sponsors]),
                application_financing_republic_grant
            )

            obj = {
                "municipal_district": municipal_district.RegionNameE,
                "settlement_count": settlement_count,
                "application_count": application_count,
                "settlement_app_percent": self.get_percentage(application_count, settlement_count),
                "application_winner_count": application_winner_count,
                "application_winner_percent": application_winner_percent,
                "application_financing_settlement_budget": application_financing_settlement_budget,
                "application_financing_people": application_financing_people,
                "application_financing_sponsors": application_financing_sponsors,
                "application_financing_republic_grant": application_financing_republic_grant,
                "application_finded_sum_percent": application_finded_sum_percent,
            }
            d.append(obj)
        ser = Application_stat_by_district_serializer(d, many=True).data
        result['data'] = ser
        return Response(result)

    def get_percentage(self, val1, val2):
        if val2 == 0:
            return 0
        return (val1 * 100) / val2

    def get_financing_settlement_budget(self, obj: Application):
        result = 0
        for app in obj:
            result += app.get_financing_settlement_budget()
        return result

    def get_financing_people(self, obj: Application):
        result = 0
        for app in obj:
            result += app.get_financing_people()
        return result

    def get_financing_sponsors(self, obj: Application):
        result = 0
        for app in obj:
            result += app.get_financing_sponsors()
        return result

    def get_financing_republic_grant(self, obj: Application):
        result = 0
        for app in obj:
            result += app.get_financing_republic_grant()
        return result
