from rest_framework.views import Request, Response

from apps.constructor.models import Application
from apps.constructor.classificators_models import Contest
from ..serializers import Applications_serializer
from .crud import update, get
from apps.history.services import create_history
from .custom_data import validate_custom_data
from .current import get_current_section
from apps.constructor.models import Status
from .document import document_validation


def update_application(request: Request, id: int) -> Response:
    data = request.data
    validate_custom_data(request)
    document_validation(request)
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


def win_lose_calculation(request: Request) -> list:
    section = get_current_section(request)
    obj = Application.objects.filter(section=section)
    grant_sum = Contest.objects.get(section=section).grant_sum
    result = []
    for i in obj:
        req_sum = i.get_financing_republic_grant()
        grant_sum = grant_sum - req_sum
        if grant_sum < 0:
            result.append(
                {
                    "id": i.id,
                    "status": "loose"
                }
            )
        else:
            result.append(
                {
                    "id": i.id,
                    "status": "win"
                }
            )
    return result
