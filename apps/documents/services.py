from rest_framework.views import Request, Response
from copy import deepcopy

from services.crud_services import Base_crud
from .serializer import Document_serializer
from .models import Document
from services.current import get_current_section


def create_document(request: Request):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request).id
    return Response(Base_crud.create(Document_serializer, data))


def get_all_documents(request: Request):
    return Response(Base_crud.get_many(Document, Document_serializer, {'section': get_current_section(request)}))


def update_document(request: Request, id: int):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request).id
    return Response(Base_crud.patch(Document, Document_serializer, data, {"id": id}))
