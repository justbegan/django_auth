from rest_framework.views import Request, Response
from deepdiff import DeepDiff
from copy import deepcopy
import logging

from .serializers import History_serializer
from apps.constructor.api.services.crud import create
from apps.constructor.models import Application


logger = logging.getLogger('django')


def get_histories_by_application_id(request: Request, id: int):
    instance = Application.objects.get(id=id)
    history = instance.history.all()
    changes = []
    for i in range(1, len(history)):
        new_record = history[i - 1]
        old_record = history[i]
        delta = new_record.diff_against(old_record)
        for change in delta.changes:
            change_data = {
                "field": change.field,
                "new": change.new,
                "old": change.old,
                "автор": new_record.history_user.username if new_record.history_user else "Unknown"
            }
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
