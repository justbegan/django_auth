from rest_framework.views import Request, Response

from .current import get_current_section
from .crud import create, update, get_many
from ..serializers import Contest_serializer
from ...models import Contest


def create_contest(request: Request):
    return Response(create(Contest_serializer, request.data))


def update_contest(request: Request, id: int):
    return Response(update(Contest, Contest_serializer, request.data, {"id": id}))


def get_contests_by_section(request: Request):
    section = get_current_section(request)
    return Response(get_many(Contest, Contest_serializer, {"section": section}))
