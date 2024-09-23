from rest_framework.views import Response, Request
from django.db.models import Model
from django.contrib.contenttypes.models import ContentType

from ..serializers import Main_table_fields_serializer
from ..models import Main_table_fields
from .current import get_current_section
from services.crud import get_many


def get_main_table_fields_by_section_method(request: Request, model: Model):
    section = get_current_section(request)
    content_type = ContentType.objects.get_for_model(model)
    print(content_type)
    return get_many(Main_table_fields, Main_table_fields_serializer,
                    {"section": section, "content_type": content_type}, 'pos')


def get_main_table_fields_by_section(request: Request):
    return Response(get_main_table_fields_by_section_method(request))
