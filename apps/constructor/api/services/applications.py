from rest_framework.views import Request, Response

from apps.constructor.models import Application
from ..serializers import Applications_serializer
from .crud import update, get
from apps.history.services import create_history
from apps.constructor.models import Status


def update_application(request: Request, id: int) -> Response:
    data = request.data
    obj = update(Application, Applications_serializer, data, {"id": id})
    if obj:
        try:
            status_title = Status.objects.get(id=data['status']).title
            history_data = {
                "author": request.user.id,
                "text": f"Статус заявки изменен на {status_title}",
                "application": obj["id"]
            }
            create_history(history_data)
        except:
            pass
    return Response(obj)


def get_by_application_id(request: Request, id: int) -> Response:
    return Response(
        get(Application, Applications_serializer, {"id": id})
    )
