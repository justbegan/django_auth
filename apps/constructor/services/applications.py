from rest_framework.views import Request, Response
from decimal import Decimal
from copy import deepcopy
from django.db import transaction
from jsonschema import validate, ValidationError, draft7_format_checker
from rest_framework.serializers import ModelSerializer
from django.db.models import Model
from abc import ABC, abstractmethod
from django.db.models.expressions import RawSQL
from django.contrib.contenttypes.models import ContentType
import logging
from django.db.models import Sum, ExpressionWrapper, F, Window, DecimalField
from django.db.models.functions import RowNumber

from apps.constructor.models import Contest, Application, Schema, Status, Calculated_fields
from ..serializers import Application_for_map_serializer, Schema_serializer
from services.crud_services import Base_crud
from services.current import (get_current_section, get_current_contest, get_current_profile,
                              get_current_win_status, get_current_lose_status, get_current_new_status)
from apps.comments.services import create_comment_and_change_status
from ..serializers import Applications_serializer
from .decorators import status_validator
from apps_modules.calculation.models import Formula


logger = logging.getLogger('django')


class CustomDataValidationError(Exception):
    pass


class SchemaNotFoundError(Exception):
    pass


class Base_application_services(ABC):
    model: Model = None
    serializer: ModelSerializer = None
    status: Status = None
    schema: Schema = None

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
            {
                "schema": cls.get_schema(id),
                "app": Base_crud.get(cls.model, cls.serializer, {"id": id}, {"request": request})
            }
        )

    @classmethod
    def get_schema(cls, app_id: int) -> Response:
        contest = cls.model.objects.get(id=app_id).contest
        schema = cls.schema.objects.filter(contests=contest).first()
        data = Schema_serializer(schema).data
        return data

    @classmethod
    @abstractmethod
    def validate_custom_data(cls, request: Request):
        pass


class Application_services(Base_application_services):
    model = Application
    serializer = Applications_serializer
    status = Status
    schema = Schema
    formula = Formula

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
        schema_data = cls.schema.objects.filter(section=get_current_section(request)).values().last()

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
            result = []
            try:
                data = sorted(data, key=lambda x: (x['created_at'], -x['total_point']))
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

    @classmethod
    def query_handler(cls, request: Request, query: dict) -> dict:
        section = get_current_section(request)
        profile = get_current_profile(request)
        content_type = ContentType.objects.get_for_model(Application)

        try:
            query = query.annotate(
                **{
                    field.title: Sum(RawSQL(field.code, [])) for field in Calculated_fields.objects.filter(
                        section=section,
                        content_type=content_type,
                        func_type=1,
                        contest=F('contest')
                    )
                }
            )

        except Exception as e:
            logger.exception(f"Ошибка выполнения sql запроса в кастомных полях заявки {e}")
        section = get_current_section(request)
        if section.modules.filter(verbose_name='Calculation').exists():
            query = query.annotate(
                total_point=ExpressionWrapper(
                    cls.get_formula_by_contest(F('contest')),
                    output_field=DecimalField(max_digits=20, decimal_places=2)
                )
            ).annotate(
                rating=Window(
                    expression=RowNumber(),
                    order_by=[F('total_point').desc(), F('created_at').asc()]
                )
            )

        if profile.role.title == 'moderator' or profile.role.title == 'admin':
            return query.filter(contest__section=section).order_by('-created_at')
        else:
            return query.filter(author=profile).order_by('-id')

    @classmethod
    def get_formula_by_contest(cls, contest):
        fields = cls.formula.objects.filter(contest__id=contest).last().json
        expression = F(fields[0])
        for field in fields[1:]:
            expression += F(field)
        return expression
