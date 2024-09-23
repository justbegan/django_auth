from rest_framework.views import APIView, Response, Request
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from apps.constructor.models import Application
from .serializers import (Application_registry_serializer, Results_of_applications_acceptance_serializer,
                          Application_rating_serializer)
from apps.constructor.services.current import get_current_section
from .filter import Application_rating_filter


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
