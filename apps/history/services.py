from rest_framework.views import Request, Response
from deepdiff import DeepDiff
from copy import deepcopy
import logging
from django.core.exceptions import ObjectDoesNotExist
from dictdiffer import diff

from .serializers import History_serializer
from apps.constructor.api.services.crud import create
from apps.constructor.models import Application, Schema


logger = logging.getLogger('django')


def get_field_description(field_name: str) -> str:
    try:
        # Получаем поле модели по его имени
        field = Application._meta.get_field(field_name)
        # Возвращаем verbose_name поля
        return field.verbose_name
    except ObjectDoesNotExist:
        # Если поле не найдено, возвращаем None
        return field_name


def get_custom_field_description(schema: Schema, field_data: dict) -> str:
    result = {}
    fields = schema.get(id=1).properties
    for k, v in field_data.items():
        field = fields.get(k)
        if field:
            result[field['title']] = v
        else:
            result[k] = v
    return result


def get_histories_by_application_id(request: Request, id: int):
    # schema = Schema.objects
    instance = Application.objects.get(id=id)
    history = instance.history.all()
    changes = []
    for i in range(1, len(history)):
        new_record = history[i - 1]
        old_record = history[i]
        delta = new_record.diff_against(old_record)

        for change in delta.changes:
            change_data = {
                "time": new_record.history_date,
                "field": get_field_description(change.field),
                "author": new_record.history_user.username if new_record.history_user else "Unknown"
            }
            if change.field == 'custom_data':
                # Сравниваем данные
                differences = diff(change.old, change.new)

                # Преобразуем результат в словарь
                diff_dict = {
                    change[0]: {change[1]: change[2]} for change in differences
                }
                change_data["test"] = diff_dict
            else:
                change_data["new"] = change.new
                change_data["old"] = change.old
            changes.append(change_data)
    return Response(changes)


def create_history(request: Request, new: dict, created: bool = False):
    try:
        old = deepcopy(request.data)
        data = {
            "application": new["id"],
            "author": request.user.id
        }
        if created:
            data["diff"] = {"created": True}
        else:
            print(DeepDiff(old, new))
            data["diff"] = DeepDiff(old, new)
    except Exception as e:
        logger.exception(f"Ошибка при создании истории в заявке № {new.id} {e}")

    return Response(create(History_serializer, data))
