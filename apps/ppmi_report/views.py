from rest_framework.views import APIView, Response, Request

from apps.constructor.models import Application
from .serializers import Application_registry_serializer
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
