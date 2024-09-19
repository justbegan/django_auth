from rest_framework.views import Request, Response
from copy import deepcopy

from ..models import Meeting_app
from ..serializers import Meeting_app_serializer
from services.crud import update, get
from .custom_data import validate_custom_data
from .document import document_validation
from .current import get_current_contest


def update_meeting_application(request: Request, id: int) -> Response:
    data = deepcopy(request.data)
    instance = Meeting_app.objects.get(id=id)
    data['author'] = instance.author.id
    data['section'] = instance.section.id
    data['contest'] = get_current_contest(request).id
    data['custom_data'] = validate_custom_data(request)
    document_validation(request)
    return Response(update(Meeting_app, Meeting_app_serializer, data, {"id": id}))


def get_by_meeting_application_id(request: Request, id: int) -> Response:
    return Response(
        get(Meeting_app, Meeting_app_serializer, {"id": id})
    )
