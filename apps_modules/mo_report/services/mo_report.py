from apps.constructor.services.applications import Application_services
from rest_framework.views import Request, Response
from copy import deepcopy
from django.db import transaction
from jsonschema import validate, ValidationError, draft7_format_checker

from services.crud import create, patch, get
from apps.constructor.services.current import (get_current_section, get_current_contest, get_current_profile)
from apps.comments.services import create_comment_and_change_status
from ..models import Mo_report_app, Mo_report_schema
from ..serializers import Mo_report_app_serializer


class Mo_report_services(Application_services):
    @staticmethod
    def create_application(request: Request) -> Response:
        request.data['author'] = get_current_profile(request).id
        request.data['section'] = get_current_section(request).id
        request.data['contest'] = get_current_contest(request).id
        request.data['custom_data'] = Mo_report_services.validate_custom_data(request)
        return Response(create(Mo_report_app_serializer, request.data))

    @staticmethod
    @transaction.atomic
    def update_application(request: Request, id: int) -> Response:
        data = deepcopy(request.data)
        Mo_report_services.validate_custom_data(request)
        obj = patch(Mo_report_app, Mo_report_app_serializer, data, {"id": id})
        comment = data.get("comment")
        if comment:
            create_comment_and_change_status(request, comment, id)
        return Response(obj)

    @staticmethod
    def get_by_application_id(request: Request, id: int) -> Response:
        return Response(
            get(Mo_report_app, Mo_report_app_serializer, {"id": id})
        )

    @staticmethod
    def validate_custom_data(request: Request):
        data = deepcopy(request.data)
        custom_data = data.get("custom_data")
        if not isinstance(custom_data, dict):
            raise Exception({"custom_data": f"Ожидалось dict, получено {type(custom_data).__name__}."})
        schema = Mo_report_schema.objects.filter(section=get_current_section(request)).values().last()
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
