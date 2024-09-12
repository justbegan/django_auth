from rest_framework.views import Request, Response
from decimal import Decimal
from copy import deepcopy
from django.db import transaction

from apps.constructor.models import Application
from apps.constructor.classificators_models import Contest
from ..serializers import Applications_serializer
from .crud import update, get
from .custom_data import validate_custom_data
from .current import get_current_section
from .document import document_validation
from apps.comments.services import create_comment_and_change_status


@transaction.atomic
def update_application(request: Request, id: int) -> Response:
    data = deepcopy(request.data)
    validate_custom_data(request)
    document_validation(request)
    obj = update(Application, Applications_serializer, data, {"id": id})
    comment = data.get("comment")
    if comment:
        create_comment_and_change_status(request, comment, id)
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
