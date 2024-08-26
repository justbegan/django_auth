from rest_framework.views import Request, Response

from apps.constructor.models import Application
from ..serializers import Applications_serializer
from .crud import update, get


def update_application(request: Request, id: int) :
    data = request.data
    return Response(
        update(Application, Applications_serializer, data, {"id": id})
    )
    

def get_by_application_id(request: Request, id: int):
    return Response(
        get(Application, Applications_serializer, {"id": id})
    )