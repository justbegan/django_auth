from rest_framework.views import Response, Request
from django.db.models import Model
from django.contrib.contenttypes.models import ContentType
from django.db.models import F

from .serializers import Main_table_fields_serializer
from .models import Main_table_fields
from apps.constructor.services.current import get_current_section
from services.crud import get_many


def get_main_table_fields_by_section_method(request: Request = None, model: Model = None, section_obj: dict = None):
    if section_obj:
        section = section_obj
    else:
        section = get_current_section(request)
    content_type = ContentType.objects.get_for_model(model)
    obj = get_many(Main_table_fields, Main_table_fields_serializer,
                   {"section": section, "content_type": content_type}, 'pos')
    result = []
    for i in obj:

        if i.get('filter') and i.get('filter_type') == 1:
            content_type = ContentType.objects.get(id=i['filter_class'])
            model_class = content_type.model_class()
            filter_config = i.get('filter_config', None)
            if filter_config:
                config_current_section = filter_config.get('current_section', False)
                config_filter = i['filter_config'].get('filter', {})
                # если в справочнике есть параметр секция
                if config_current_section:
                    config_filter['section'] = section.id
                mapping_conf = i['filter_config'].get('mapping', {})
                annotations = {
                    new_field: F(old_field) for new_field, old_field in mapping_conf.items()
                }
                i['filter_data'] = model_class.objects.annotate(
                    **annotations).filter(**config_filter).values("id", "title")
            else:
                i['filter_data'] = model_class.objects.values("id", "title")

        elif i.get('filter') and i.get('filter_type') == 2:
            i['filter_data'] = i['filter_custom_data']
        result.append(i)
    return result


def get_main_table_fields_by_section(request: Request):
    return Response(get_main_table_fields_by_section_method(request))
