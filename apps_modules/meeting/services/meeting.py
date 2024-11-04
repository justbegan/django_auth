from rest_framework.views import Request, Response
from copy import deepcopy
from django.db import transaction

from apps.constructor.services.current import (get_current_section, get_current_contest, get_current_profile)
from apps.constructor.services.custom_data import validate_custom_data
from services.crud import create, patch, get
from ..models import Meeting_app, Status, Meeting_schema
from ..serializers import Meeting_app_serializer
from apps.comments.services import create_comment_and_change_status


class Meeting_services:
    @staticmethod
    def create_application(request: Request) -> Response:
        request.data['author'] = get_current_profile(request).id
        request.data['section'] = get_current_section(request).id
        request.data['contest'] = get_current_contest(request).id
        request.data['custom_data'] = validate_custom_data(request, Status, Meeting_schema)
        return Response(create(Meeting_app_serializer, request.data))

    @staticmethod
    @transaction.atomic
    def update_application(request: Request, id: int) -> Response:
        data = deepcopy(request.data)
        validate_custom_data(request, Status, Meeting_schema)
        obj = patch(Meeting_app, Meeting_app_serializer, data, {"id": id})
        comment = data.get("comment")
        if comment:
            create_comment_and_change_status(request, comment, id)
        return Response(obj)

    @staticmethod
    def get_by_application_id(request: Request, id: int) -> Response:
        return Response(
            get(Meeting_app, Meeting_app_serializer, {"id": id})
        )
