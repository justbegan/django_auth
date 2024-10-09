from rest_framework.views import Request

from ..models import Meeting_app
from apps.constructor.services.applications import create_application
from apps.constructor.serializers import Applications_serializer
from apps.constructor.services.current import get_current_new_status


def create_app(request: Request, meeting_id: int):
    meeting = Meeting_app.objects.get(id=meeting_id)
    request.data['municipal_district'] = meeting.municipal_district.id
    request.data['settlement'] = meeting.settlement.id
    request.data['locality'] = meeting.locality.id
    request.data['custom_data'] = {}
    request.data['title'] = meeting.get_selected_project()
    request.data['status'] = get_current_new_status(request).id
    return create_application(request, Applications_serializer)
