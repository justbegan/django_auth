from rest_framework.views import Request, Response
from decimal import Decimal

from apps.constructor.models import Application
from apps.constructor.classificators_models import Contest
from ..serializers import Applications_serializer
from .crud import update, get
from .custom_data import validate_custom_data
from .current import get_current_section
from .document import document_validation


def update_application(request: Request, id: int) -> Response:
    data = request.data
    validate_custom_data(request)
    document_validation(request)
    obj = update(Application, Applications_serializer, data, {"id": id})
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
        grant_sum = grant_sum - Decimal(req_sum)
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
