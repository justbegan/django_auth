from rest_framework.views import Request, Response
from copy import deepcopy
from rest_framework.serializers import ModelSerializer
from django.db.models import Model

from ..models import Status
from ..serializers import Status_serializer
from services.crud_services import Base_crud
from services.current import get_current_section


class Base_status_services:
    model: Model = None
    serializer: ModelSerializer = None

    @classmethod
    def get_all_statuses_by_section(cls, request: Request):
        return Response(Base_crud.get_many(cls.model, cls.serializer, {"section": get_current_section(request)}))

    @classmethod
    def update_status(cls, request: Request, id: int):
        data = deepcopy(request.data)
        instance = cls.model.objects.get(id=id)
        data['section'] = instance.section.id
        return Response(Base_crud.update(cls.model, cls.serializer, request.data, {"id": id}))

    @classmethod
    def create_status(cls, request: Request):
        data = deepcopy(request.data)
        data['section'] = get_current_section(request)
        return Response(Base_crud.create(cls.serializer, request.data))

    @classmethod
    def delete_status(cls, request: Request, id: int):
        return Response(Base_crud.delete(cls.model, {"id": id}))

    @classmethod
    def get_status_by_name(cls, request: Request, name: str):
        return Response(
            Base_crud.get(cls.model, cls.serializer, {"tech_name": name, "section": get_current_section(request)})
        )


class Status_serives(Base_status_services):
    model = Status
    serializer = Status_serializer
