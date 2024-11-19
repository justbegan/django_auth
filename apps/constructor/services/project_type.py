from rest_framework.views import Request, Response
from copy import deepcopy

from ..models import Project_type
from ..serializers import Project_type_serializer
from services.crud_services import Base_crud
from services.current import get_current_section


def get_project_type_by_section(request: Request):
    return Response(Base_crud.get_many(
        Project_type, Project_type_serializer, {"section": get_current_section(request)}))


def create_project_type(request: Request):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request).id
    return Response(Base_crud.create(Project_type_serializer, data))


def update_project_type(request: Request, id: int):
    data = deepcopy(request.data)
    instance = Project_type.objects.get(id=id)
    data['section'] = instance.section.id
    return Response(Base_crud.update(Project_type, Project_type_serializer, data, {"id": id}))


def delete_project_type(request: Request, id: int):
    return Response(Base_crud.delete(Project_type, {"id": id}))
