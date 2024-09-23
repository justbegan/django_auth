from rest_framework.views import Response, Request
from ..services.current import get_current_section
from services.crud import create, get_many, update, delete
from copy import deepcopy

from ..serializers import Document_type_serializer
from ..models import Document_type


def create_document_type(request: Request):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request)
    return Response(create(Document_type_serializer, data))


def get_all_document_types_by_section(request: Request):
    section = get_current_section(request)
    return Response(get_many(Document_type, Document_type_serializer, {'section': section}))


def update_document_type(request: Request, id: int):
    data = deepcopy(request.data)
    instance = Document_type.objects.get(id=id)
    data['section'] = instance.section.id
    return Response(update(Document_type, Document_type_serializer, data, {"id": id}))


def delete_document_type(request: Request, id: int):
    return Response(delete(Document_type, {"id": id}))
