from rest_framework.views import Request, Response
from copy import deepcopy
from rest_framework.serializers import ModelSerializer
from django.db.models import Model

from ..serializers import Status_serializer
from ..models import Status
from services.crud import get_many, update, create, delete
from .current import get_current_section


def get_all_statuses_by_section(request: Request, model: Model, serializer: ModelSerializer):
    return Response(get_many(model, serializer, {"section": get_current_section(request)}))


def update_status(request: Request, id: int):
    data = deepcopy(request.data)
    instance = Status.objects.get(id=id)
    data['section'] = instance.section.id
    return Response(update(Status, Status_serializer, request.data, {"id": id}))


def create_status(request: Request):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request)
    return Response(create(Status_serializer, request.data))


def delete_status(request: Request, id: int):
    return Response(delete(Status, {"id": id}))
