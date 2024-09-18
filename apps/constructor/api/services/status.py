from rest_framework.views import Request, Response
from copy import deepcopy

from ..serializers import Status_serializer
from ...models import Status
from services.crud import get_many, update, create
from .current import get_current_section


def get_all_statuses_by_section(request: Request):
    return Response(get_many(Status, Status_serializer, {"section": get_current_section(request)}))


def update_status(request: Request, id: int):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request)
    return Response(update(Status, Status_serializer, request.data, {"id": id}))


def create_status(request: Request):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request)
    return Response(create(Status_serializer, request.data))
