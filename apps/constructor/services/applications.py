from rest_framework.views import Request, Response
from decimal import Decimal
from copy import deepcopy
from django.db import transaction

from apps.constructor.models import Contest, Application, Schema, Status
from ..serializers import Application_for_map_serializer
from services.crud import get, create, patch
from .custom_data import validate_custom_data
from .current import (get_current_section, get_current_contest, get_current_profile,
                      get_current_win_status, get_current_lose_status)
from apps.comments.services import create_comment_and_change_status
from ..serializers import Applications_serializer


class Application_services:
    @staticmethod
    def create_application(request: Request) -> Response:
        request.data['author'] = get_current_profile(request).id
        request.data['section'] = get_current_section(request).id
        request.data['contest'] = get_current_contest(request).id
        request.data['custom_data'] = validate_custom_data(request, Status, Schema)
        return Response(create(Applications_serializer, request.data))

    @staticmethod
    @transaction.atomic
    def update_application(request: Request, id: int) -> Response:
        data = deepcopy(request.data)
        validate_custom_data(request, Status, Schema)
        obj = patch(Application, Applications_serializer, data, {"id": id})
        comment = data.get("comment")
        if comment:
            create_comment_and_change_status(request, comment, id)
        return Response(obj)

    @staticmethod
    def get_by_application_id(request: Request, id: int) -> Response:
        return Response(
            get(Application, Applications_serializer, {"id": id})
        )

    @staticmethod
    def win_lose_calculation(request: Request, data: list) -> list:
        section = get_current_section(request)
        if section.modules.filter(verbose_name='Calculation').exists():
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
        return []

    @staticmethod
    def application_for_map(queryset: list, request: Request) -> list:
        return Response(Application_for_map_serializer(queryset, many=True).data)

    @staticmethod
    def change_applications_statuses_to_win(request: Request, contest_id: int):
        section = get_current_section(request)
        data = Application.objects.filter(section=section, contest__id=contest_id)
        if section.modules.filter(verbose_name='Calculation').exists():
            all_contests = Contest.objects.filter(section=section)
            data = sorted(data, key=lambda x: (x.created_at, -x.total_point()))
            try:
                for contest in all_contests:
                    grant_sum = contest.grant_sum
                    for app in data:
                        if contest.id == app.contest_id:
                            req_sum = app.get_financing_republic_grant()
                            grant_sum -= Decimal(req_sum)
                            if grant_sum >= 0:
                                app.status = get_current_win_status(request)
                            else:
                                app.status = get_current_lose_status(request)
                            app.save()

                return Response({"message": True})

            except Exception as e:
                return Response({"message": str(e)})
        return Response({"message": "Модуль не найден"})
