from rest_framework.views import APIView, Response, Request
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models.expressions import RawSQL
from django.db.models import Sum

from apps.constructor.models import Application
from .serializers import (Ppmi_report_base_serializer, Application_stat_by_district_serializer)
from .filter import Application_rating_filter
from apps.locations.models import Municipal_district, Settlement
from .services import Ppmi_report_services, Base_pagination


class Application_registry_pagination(Base_pagination):
    def get_fields(self):
        return {
            'municipal_district': 'Район',
            'settlement': 'Поселение',
            'locality': 'Населенный пункт',
            'title': 'Название проекта',
            'project_type': 'Типология проекта',
            'total_price': 'Стоимость проекта'
        }


class Application_registry(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Application.objects.all().order_by('-id')
    pagination_class = Application_registry_pagination
    serializer_class = Ppmi_report_base_serializer

    def get_queryset(self):
        return Ppmi_report_services.query_handler(self.request, super().get_queryset())


class Results_of_applications_acceptance_pagination(Base_pagination):
    def get_fields(self):
        return {
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
        }


class Results_of_applications_acceptance(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Application.objects.all().order_by('-id')
    pagination_class = Results_of_applications_acceptance_pagination
    serializer_class = Ppmi_report_base_serializer

    def get_queryset(self):
        return Ppmi_report_services.query_handler(self.request, super().get_queryset())


class Application_rating_pagination(Base_pagination):
    def get_fields(self):
        return {
            'municipal_district': 'Район',
            'settlement': 'Поселение',
            'locality': 'Населенный пункт',
            'title': 'Название проекта',
            'rating': 'Рейтинг',
            'get_financing_republic_grant': 'Сумма субсидии',
            'total_point': 'Итог. балл'
        }


class Application_rating(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Application.objects.all().order_by('-id')
    pagination_class = Results_of_applications_acceptance_pagination
    serializer_class = Ppmi_report_base_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = Application_rating_filter

    def get_queryset(self):
        return Ppmi_report_services.query_handler(
            self.request, super().get_queryset()
        ).order_by('total_point', 'created_at')


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
            'section__id': 1
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
        objects = []
        application_financing_settlement_budget_sql = """
SELECT
    (element ->> 'price')::decimal AS price
FROM
    jsonb_array_elements(custom_data->'planned_finansing_sources') AS element
WHERE
    element ->> 'source_type' = 'Бюджет поселения (муниципального района) (не менее 5 процентов\
 от суммы субсидии из республиканского бюджета)'
        """
        application_financing_people_sql = """
SELECT
    (element ->> 'price')::decimal AS price
FROM
    jsonb_array_elements(custom_data->'planned_finansing_sources') AS element
WHERE
    element ->> 'source_type' = 'Население (поступления от жителей)'
        """
        application_financing_sponsors_sql = """
SELECT
    (element ->> 'price')::decimal AS price
FROM
    jsonb_array_elements(custom_data->'planned_finansing_sources') AS element
WHERE
    element ->> 'source_type' = 'Спонсоры (денежные поступления от юр.лиц, инд.предпринимателей и т.д.)'
        """
        application_financing_republic_grant_sql = """
SELECT
    (element ->> 'price')::decimal AS price
FROM
    jsonb_array_elements(custom_data->'planned_finansing_sources') AS element
WHERE
    element ->> 'source_type' = 'Субсидия из бюджета Республики Саха (Якутия) на софинансирование проектов развития\
 общественной инфраструктуры, основанных на местных инициативах'
        """
        for municipal_district in Municipal_district.objects.all():
            app_by_md = application_obj.filter(municipal_district=municipal_district)
            settlement_count = settlement_obj.filter(RegID=municipal_district).count()
            application_count = application_obj.filter(municipal_district=municipal_district).count()
            application_winner_count = application_obj.filter(
                municipal_district=municipal_district, status__title="Победила").count()
            application_winner_percent = self.get_percentage(application_winner_count, application_count)
            application_financing_settlement_budget = self.get_field_value(
                app_by_md,
                application_financing_settlement_budget_sql
            )
            application_financing_people = self.get_field_value(
                app_by_md,
                application_financing_people_sql
            )
            application_financing_sponsors = self.get_field_value(
                app_by_md,
                application_financing_sponsors_sql
            )
            application_financing_republic_grant = self.get_field_value(
                app_by_md,
                application_financing_republic_grant_sql
            )
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
            objects.append(obj)
        ser = Application_stat_by_district_serializer(objects, many=True).data
        result['data'] = ser
        return Response(result)

    def get_percentage(self, val1, val2):
        if val2 == 0:
            return 0
        return (val1 * 100) / val2

    def get_field_value(self, app: Application, sql: str):
        return app.aggregate(total=Sum(RawSQL(sql, [])))['total']
