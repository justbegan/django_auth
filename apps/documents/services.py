from rest_framework.views import Request, Response

from services.crud import create, get_many, update
from .serializer import Document_serializer
from .models import Document


def create_document(request: Request):
    return Response(create(Document_serializer, request.data))


def get_all_documents(request: Request):
    return Response(get_many(Document, Document_serializer))


def update_document(request: Request, id: int):
    return Response(update(Document, Document_serializer, request.data, {"id": id}))
