from rest_framework.views import Response, Request
from services.current import get_current_section
from services.crud_services import Base_crud
from copy import deepcopy
from django.db.models import Model
from rest_framework.serializers import ModelSerializer

from ..serializers import Document_type_serializer
from ..models import Document_type


class Document_type_base_services:
    model: Model = None
    serializer: ModelSerializer = None

    @classmethod
    def create_document_type(cls, request: Request):
        data = deepcopy(request.data)
        data['section'] = get_current_section(request)
        return Response(Base_crud.create(cls.serializer, data))

    @classmethod
    def get_all_document_types_by_section(cls, request: Request):
        section = get_current_section(request)
        return Response(Base_crud.get_many(cls.model, cls.serializer, {'section': section}))

    @classmethod
    def update_document_type(cls, request: Request, id: int):
        data = deepcopy(request.data)
        instance = cls.model.objects.get(id=id)
        data['section'] = instance.section.id
        return Response(Base_crud.update(cls.model, cls.serializer, data, {"id": id}))

    @classmethod
    def delete_document_type(cls, request: Request, id: int):
        return Response(Base_crud.delete(cls.model, {"id": id}))


class Document_type_services(Document_type_base_services):
    model = Document_type
    serializer = Document_type_serializer
