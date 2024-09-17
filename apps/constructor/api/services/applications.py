from rest_framework.views import Request, Response
from decimal import Decimal
from copy import deepcopy
from django.db import transaction

from apps.constructor.models import Application, Contest
from ..serializers import Applications_serializer, Application_for_map_serializer
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
    instance = Application.objects.get(id=id)
    data['author'] = instance.author.id
    data['section'] = instance.section.id
    data['contest'] = instance.contest.id
    obj = update(Application, Applications_serializer, data, {"id": id})
    comment = data.get("comment")
    if comment:
        create_comment_and_change_status(request, comment, id)
    return Response(obj)


def get_by_application_id(request: Request, id: int) -> Response:
    return Response(
        get(Application, Applications_serializer, {"id": id})
    )


def win_lose_calculation(request: Request, data: list) -> list:
    section = get_current_section(request)
    all_contests = Contest.objects.filter(section=section)
    result = []
    for c in all_contests:
        grant_sum = Contest.objects.get(id=c.id).grant_sum
        for i in data:
            if c.id == i["contest"]:
                req_sum = i["get_financing_republic_grant"]
                grant_sum = grant_sum - Decimal(req_sum)
                if grant_sum < 0:
                    result.append(
                        {
                            "id": i["id"],
                            "status": "loose"
                        }
                    )
                else:
                    result.append(
                        {
                            "id": i["id"],
                            "status": "win"
                        }
                    )
    return result


def application_for_map(queryset: list, request: Request) -> list:
    return Response(Application_for_map_serializer(queryset, many=True).data)
