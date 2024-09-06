from rest_framework.views import Request, Response

from ..models import Meeting_app
from ..serializers import Meeting_app_serializer
from apps.constructor.api.services.crud import update, get
from .custom_data import validate_custom_data
from .document import document_validation


def update_meeting_application(request: Request, id: int) -> Response:
    data = request.data
    validate_custom_data(request)
    document_validation(request)
    return Response(update(Meeting_app, Meeting_app_serializer, data, {"id": id}))


def get_by_meeting_application_id(request: Request, id: int) -> Response:
    return Response(
        get(Meeting_app, Meeting_app_serializer, {"id": id})
    )
