from rest_framework.views import Request, Response
from copy import deepcopy
from django.contrib.contenttypes.models import ContentType

from services.crud_services import Base_crud
from services.current import get_current_section
from ..serializers import Role_handler_serializer
from ..models import Role_handler


def create_role_handler(request: Request):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request)
    return Response(Base_crud.create(Role_handler_serializer, data))


def update_role_handler(request: Request, id: int):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request)
    return Response(Base_crud.update(Role_handler, Role_handler_serializer, data, {"id": id}))


def get_all_roles_handler(request: Request):
    return Response(Base_crud.get_many(
        Role_handler, Role_handler_serializer, {"section": get_current_section(request)}
    ))


def delete_role_handler(request: Request, id: int):
    return Response(Base_crud.delete(Role_handler, {"id": id}))


def get_role_handler_by_id(request: Request, id: int):
    return Response(Base_crud.get(Role_handler, Role_handler_serializer, {"id": id}))


def get_all_models(request: Request):
    obj = ContentType.objects.all()
    return Response(obj.values())
