from rest_framework.views import Request, Response
from decimal import Decimal
from copy import deepcopy
from django.db import transaction
from django.db.models import Model
from rest_framework.serializers import Serializer

from apps.constructor.models import Contest
from ..serializers import Application_for_map_serializer
from services.crud import update, get
from .custom_data import validate_custom_data
from .current import get_current_section, get_current_contest
from .custom_validation import custom_validation
from apps.comments.services import create_comment_and_change_status
from services.crud import create


def create_application(request: Request, serializer: Serializer) -> Response:
    request.data['author'] = request.user.id
    request.data['section'] = get_current_section(request).id
    request.data['contest'] = get_current_contest(request).id
    request.data['custom_data'] = validate_custom_data(request)
    custom_validation(request)
    return Response(create(serializer, request.data))


@transaction.atomic
def update_application(request: Request, id: int, model: Model, serializer: Serializer) -> Response:
    data = deepcopy(request.data)
    validate_custom_data(request)
    instance = model.objects.get(id=id)
    data['author'] = instance.author.id
    data['section'] = instance.section.id
    data['contest'] = instance.contest.id
    obj = update(model, serializer, data, {"id": id})
    comment = data.get("comment")
    if comment:
        create_comment_and_change_status(request, comment, id)
    return Response(obj)


def get_by_application_id(request: Request, id: int, model: Model, serializer: Serializer) -> Response:
    return Response(
        get(model, serializer, {"id": id})
    )


def win_lose_calculation(request: Request, data: list) -> list:
    section = get_current_section(request)
    all_contests = Contest.objects.filter(section=section)
    data = sorted(data, key=lambda x: (x['created_at'], -x['total_point']))
    result = []
    try:
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
    except Exception:
        return result


def application_for_map(queryset: list, request: Request) -> list:
    return Response(Application_for_map_serializer(queryset, many=True).data)
