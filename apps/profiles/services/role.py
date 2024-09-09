from rest_framework.views import Request, Response
from apps.constructor.api.services.crud import get_many, create, update, delete
from apps.constructor.api.services.current import get_current_section
from copy import deepcopy

from ..models import Roles
from ..serializers import Role_serializer


def get_all_roles_by_section(request: Request):
    return Response(get_many(Roles, Role_serializer, {"section": get_current_section(request)}))


def create_role(request: Request):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request)
    return Response(create(Role_serializer, data))


def update_role(request: Request, id: int):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request)
    return Response(update(Roles, Role_serializer, data, {"id": id}))


def delete_role(request: Request, id: int):
    return Response(delete(Roles, {"id": id}))
