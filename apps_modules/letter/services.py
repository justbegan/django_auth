from rest_framework.views import Response, Request
from copy import deepcopy

from apps.constructor.services.current import get_current_section
from services.crud import create, update, delete, get_many
from .serializers import Letter_serializer
from .models import Letter


def create_letter(request: Request):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request).id
    data['author'] = request.user.id
    return Response(create(Letter_serializer, data))


def update_letter(request: Request, id: int):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request).id
    data['author'] = request.user.id
    return Response(update(Letter, Letter_serializer, data, {"id": id}))


def delete_letter(request: Request, id: int):
    return Response(delete(Letter, {"id": id}))


def get_all_letters_by_section(request: Request):
    return Response(get_many(Letter, Letter_serializer, {"section": get_current_section(request).id}))
