from rest_framework.views import Request, Response
from decimal import Decimal
from copy import deepcopy
from django.db import transaction
from jsonschema import validate, ValidationError, draft7_format_checker
from rest_framework.serializers import ModelSerializer
from django.db.models import Model
from abc import ABC, abstractmethod

from apps.constructor.models import Contest, Application, Schema, Status
from ..serializers import Application_for_map_serializer
from services.crud_services import Base_crud
from .current import (get_current_section, get_current_contest, get_current_profile,
                      get_current_win_status, get_current_lose_status, get_current_new_status)
from apps.comments.services import create_comment_and_change_status
from ..serializers import Applications_serializer
from .decorators import status_validator


class CustomDataValidationError(Exception):
    pass


class SchemaNotFoundError(Exception):
    pass


class Base_application_services(ABC):
    model: Model = None
    serializer: ModelSerializer = None
    status: Status = None

    @classmethod
    @status_validator()
    def create_application(cls, request: Request) -> Response:
        request.data['author'] = get_current_profile(request).id
        request.data['section'] = get_current_section(request).id
        request.data['contest'] = get_current_contest(request).id
        request.data['custom_data'] = cls.validate_custom_data(request)
        return Response(Base_crud.create(cls.serializer, request.data))

    @classmethod
    @transaction.atomic
    @status_validator()
    def update_application(cls, request: Request, id: int) -> Response:
        data = deepcopy(request.data)
        cls.validate_custom_data(request)
        obj = Base_crud.patch(Application, Applications_serializer, data, {"id": id})
        comment = data.get("comment")
        if comment:
            create_comment_and_change_status(request, comment, id)
        return Response(obj)

    @classmethod
    def get_by_application_id(cls, request: Request, id: int) -> Response:
        return Response(
            Base_crud.get(cls.model, cls.serializer, {"id": id})
        )

    @classmethod
    @abstractmethod
    def validate_custom_data(cls, request: Request):
        pass


class Application_services(Base_application_services):
    model = Application
    serializer = Applications_serializer
    status = Status

    @classmethod
    def validate_custom_data(cls, request: Request):
        data = deepcopy(request.data)
        status = data.get("status", None)
        if status is None:
            raise CustomDataValidationError({"status": "Статус обязатен к заполнению."})
        required = status != get_current_new_status(Status, request).id
        custom_data = data.get("custom_data")
        if not isinstance(custom_data, dict):
            raise CustomDataValidationError({"custom_data": f"Ожидалось dict, получено {type(custom_data).__name__}."})
        schema_data = Schema.objects.filter(section=get_current_section(request)).values().last()

        if schema_data is None:
            raise SchemaNotFoundError("Схема не найдена для указанного раздела.")

        schema = deepcopy(schema_data)
        if not required:
            schema['required'] = []
        obj = {
            key: value for key, value in custom_data.items()
            if key in schema.get("properties", {}) and value != ''
        }

        try:
            validate(instance=obj, schema=schema, format_checker=draft7_format_checker)
        except ValidationError as e:
            raise CustomDataValidationError({"custom_data": str(e)})

        return obj

    @classmethod
    def win_lose_calculation(cls, request: Request, data: list) -> list:
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

    @classmethod
    def application_for_map(cls, queryset: list, request: Request) -> list:
        return Response(Application_for_map_serializer(queryset, many=True).data)

    @classmethod
    def change_applications_statuses_to_win(cls, request: Request, contest_id: int):
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
