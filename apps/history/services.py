from rest_framework.views import Request, Response
from rest_framework.exceptions import NotFound
from deepdiff import DeepDiff
from copy import deepcopy
import logging
from django.core.exceptions import ObjectDoesNotExist
import ast
import re

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


def get_custom_field_description(field_name: str) -> str:
    fields = Schema.objects.get(id=1).properties
    transcription = fields.get(field_name)
    if transcription:
        return transcription['title']
    else:
        return field_name


def custom_data_handler(data: dict):
    """
        dictionary_item_added
        dictionary_item_removed
        values_changed
    """
    result = {}
    obj = ast.literal_eval(str(data))
    for key, value in obj.items():
        if key == "dictionary_item_added" or key == "dictionary_item_removed":
            dictionary_item_added_list = []
            for i in value:
                match = re.search(r"root\['(.+?)'\]", i)
                word = match.group(1)
                dictionary_item_added_list.append(get_custom_field_description(word))
            result[key] = dictionary_item_added_list

        elif key == "values_changed":
            values_changed_dict = {}
            for k, v in value.items():
                k2 = re.search(r"root\['(.+?)'\]", k)
                word = k2.group(1)
                values_changed_dict[get_custom_field_description(word)] = v
            result[key] = values_changed_dict

    return result


def process_change(new_record, change, only_status):
    change_data = {
        "time": new_record.history_date,
        "field": get_field_description(change.field),
        "author": new_record.history_user.username if new_record.history_user else "Unknown"
    }
    if change.field == 'custom_data':
        change_data["custom_data"] = custom_data_handler(DeepDiff(change.old, change.new))
    else:
        change_data["new"] = change.new
        change_data["old"] = change.old

    if only_status and change.field != 'status':
        return None

    return change_data


def get_histories_by_application_id(request: Request, id: int, only_status: int):
    try:
        instance = Application.objects.get(id=id)
    except Application.DoesNotExist:
        raise NotFound(f"Application with id {id} not found.")

    history = instance.history.all()
    if len(history) < 2:
        return Response([])  # Если нет истории изменений

    changes = []
    for new_record, old_record in zip(history, history[1:]):
        delta = new_record.diff_against(old_record)

        for change in delta.changes:
            change_data = process_change(new_record, change, only_status)
            if change_data:
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
            data["diff"] = DeepDiff(old, new)
    except Exception as e:
        logger.exception(f"Ошибка при создании истории в заявке № {new.id} {e}")

    return Response(create(History_serializer, data))
