from rest_framework.views import Request
from copy import deepcopy
from jsonschema import validate, ValidationError, draft7_format_checker

from services.current import get_current_section
from ..models import Mo_report_app, Mo_report_schema, Status
from ..serializers import Mo_report_app_serializer
from apps.constructor.services.applications import Base_application_services


class Mo_report_services(Base_application_services):
    model = Mo_report_app
    serializer = Mo_report_app_serializer
    status = Status
    schema = Mo_report_schema

    @classmethod
    def validate_custom_data(cls, request: Request):
        data = deepcopy(request.data)
        custom_data = data.get("custom_data")
        if not isinstance(custom_data, dict):
            raise Exception({"custom_data": f"Ожидалось dict, получено {type(custom_data).__name__}."})
        schema = cls.schema.objects.filter(section=get_current_section(request)).values().last()
        schema = deepcopy(schema)
        obj = {
            key: value for key, value in custom_data.items()
            if key in schema.get("properties", {}) and value != ''
        }

        try:
            validate(instance=obj, schema=schema, format_checker=draft7_format_checker)
        except ValidationError as e:
            raise Exception({"custom_data": str(e)})
        return obj
