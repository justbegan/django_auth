from rest_framework.views import Response, Request
from copy import deepcopy

from services.current import get_current_section
from services.crud_services import Base_crud
from .serializers import Letter_serializer
from .models import Letter


def create_letter(request: Request):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request).id
    data['author'] = request.user.id
    return Response(Base_crud.create(Letter_serializer, data))


def update_letter(request: Request, id: int):
    data = deepcopy(request.data)
    return Response(Base_crud.patch(Letter, Letter_serializer, data, {"id": id}))


def delete_letter(request: Request, id: int):
    return Response(Base_crud.delete(Letter, {"id": id}))


def get_all_letters_by_section(request: Request):
    return Response(Base_crud.get_many(Letter, Letter_serializer, {"section": get_current_section(request).id}))
