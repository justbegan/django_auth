from rest_framework.views import Request, Response

from .models import History
from .serializers import History_serializer
from apps.constructor.api.services.crud import get_many, create


def get_histories_by_application_id(request: Request, id: int):
    return Response(get_many(History, History_serializer, {"application": id}))


def create_history(data: dict):
    return Response(create(History_serializer, data))
