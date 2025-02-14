from rest_framework.views import Request, Response
from services.crud_services import Base_crud
from services.current import get_current_section
from copy import deepcopy

from ..models import Roles
from ..serializers import Role_serializer


def get_all_roles_by_section(request: Request):
    return Response(Base_crud.get_many(Roles, Role_serializer, {"section": get_current_section(request)}))


def create_role(request: Request):
    data = deepcopy(request.data)
    return Response(Base_crud.create(Role_serializer, data))


def update_role(request: Request, id: int):
    data = deepcopy(request.data)
    return Response(Base_crud.update(Roles, Role_serializer, data, {"id": id}))


def delete_role(request: Request, id: int):
    return Response(Base_crud.delete(Roles, {"id": id}))
