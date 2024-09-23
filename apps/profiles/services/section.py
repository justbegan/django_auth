from rest_framework.views import Request, Response

from ..models import Section
from ..serializers import Section_serializer
from services.crud import get_many, get, create, update
from apps.constructor.services.current import get_current_section


def get_all_sections(request: Request):
    return Response(get_many(Section, Section_serializer))


def create_section(request: Request):
    return Response(create(Section_serializer, request.data))


def update_section(request: Request, id: int):
    return Response(update(Section, Section_serializer, request.data, {"id": id}))


def get_section_by_id(request: Request, id: int):
    return Response(get(Section, Section_serializer, {"id": id}))


def get_sections_by_user(request: Request):
    section = get_current_section(request)
    return Response(get(Section, Section_serializer, {"id": section.id}))
