from rest_framework.views import Request
from copy import deepcopy
from jsonschema import validate, ValidationError, draft7_format_checker

from services.current import (get_current_section, get_current_new_status)
from ..models import Meeting_app, Status, Meeting_schema
from ..serializers import Meeting_app_serializer
from apps.constructor.services.applications import Base_application_services
from apps.constructor.services.applications import Application_services


class CustomDataValidationError(Exception):
    pass


class SchemaNotFoundError(Exception):
    pass


class Meeting_services(Base_application_services):
    model = Meeting_app
    serializer = Meeting_app_serializer
    status = Status
    schema = Meeting_schema

    @classmethod
    def validate_custom_data(cls, request: Request):
        data = deepcopy(request.data)
        status = data.get("status", None)
        if status is None:
            raise CustomDataValidationError({"status": "Статус обязатен к заполнению."})
        required = status != get_current_new_status(Status, request).id
        custom_data = data.get("custom_data")
        if not isinstance(custom_data, dict):
            raise CustomDataValidationError({"custom_data": f"Ожидалось dict, получено {type(custom_data).__name__}."})
        schema_data = cls.schema.objects.filter(section=get_current_section(request)).values().last()

        if schema_data is None:
            raise SchemaNotFoundError("Схема не найдена для указанного раздела.")

        schema = deepcopy(schema_data)
        if not required:
            schema['required'] = []
        obj = {
            key: value for key, value in custom_data.items()
            if key in schema.get("properties", {}) and value != ''
        }

        try:
            validate(instance=obj, schema=schema, format_checker=draft7_format_checker)
        except ValidationError as e:
            raise CustomDataValidationError({"custom_data": str(e)})

        return obj

    @classmethod
    def create_app(cls, request: Request, meeting_id: int):
        meeting: Meeting_app = cls.model.objects.get(id=meeting_id)
        request.data['municipal_district'] = meeting.municipal_district.id
        request.data['settlement'] = meeting.settlement.id
        request.data['locality'] = meeting.locality.id
        request.data['custom_data'] = {}
        request.data['title'] = meeting.get_selected_project()
        request.data['status'] = get_current_new_status(Status, request).id
        return Application_services.create_application(request)
