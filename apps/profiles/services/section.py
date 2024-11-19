from rest_framework.views import Request, Response

from ..models import Section
from ..serializers import Section_serializer
from services.crud import get_many, get, create, update
from apps.constructor.services.current import get_current_section
from apps.table_fields_manager.services import get_main_table_fields_by_section_method


def get_all_sections(request: Request):
    obj = get_many(Section, Section_serializer)
    result = []
    for i in obj:
        section = Section.objects.get(id=i['id'])
        result.append(
            {
                "data": i,
                "profile_table_fields": get_main_table_fields_by_section_method(model=Section, section_obj=section)
            }
        )
    return Response(
        result
    )


def create_section(request: Request):
    return Response(create(Section_serializer, request.data))


def update_section(request: Request, id: int):
    return Response(update(Section, Section_serializer, request.data, {"id": id}))


def get_section_by_id(request: Request, id: int):
    return Response(get(Section, Section_serializer, {"id": id}))


def get_sections_by_user(request: Request):
    section = get_current_section(request)
    return Response(
        {
            "data": get(Section, Section_serializer, {"id": section.id}),
            "profile_table_fields": get_main_table_fields_by_section_method(model=Section, section_obj=section)
        }
    )
