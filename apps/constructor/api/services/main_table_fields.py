from rest_framework.views import Response, Request

from ..serializers import Main_table_fields_serializer
from ...models import Main_table_fields
from .current import get_current_section
from .crud import get_many


def get_main_table_fields_by_section_method(request: Request):
    section = get_current_section(request)
    return get_many(Main_table_fields, Main_table_fields_serializer, {"section": section})


def get_main_table_fields_by_section(request: Request):
    return Response(get_main_table_fields_by_section_method(request))
