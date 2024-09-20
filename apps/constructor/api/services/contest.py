from rest_framework.views import Request, Response
from copy import deepcopy

from .current import get_current_section
from services.crud import create, update, get_many
from ..serializers import Contest_serializer
from ...models import Contest


def create_contest(request: Request):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request)
    return Response(create(Contest_serializer, data))


def update_contest(request: Request, id: int):
    data = deepcopy(request.data)
    instance = Contest.objects.get(id=id)
    data['section'] = instance.section.id
    return Response(update(Contest, Contest_serializer, data, {"id": id}))


def get_contests_by_section(request: Request):
    section = get_current_section(request)
    return Response(get_many(Contest, Contest_serializer, {"section": section}))


def get_contest_by_year(request: Request, year: int):
    section = get_current_section(request)
    return Response(get_many(Contest, Contest_serializer, {"section": section, "year": year}))
