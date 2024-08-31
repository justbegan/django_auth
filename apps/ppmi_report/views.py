from rest_framework.views import APIView, Response, Request

from apps.constructor.models import Application
from .serializers import (Application_registry_serializer, Results_of_applications_acceptance_serializer)
from apps.constructor.api.services.current import get_current_section


class Application_registry(APIView):
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
