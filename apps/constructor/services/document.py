from rest_framework.exceptions import ValidationError
import logging
from functools import wraps
from django.db.models import Model

from services.current import get_current_section, get_current_new_status
from ..models import Status


logger = logging.getLogger('django')


def document_validation(document_type: Model):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            try:
                docs = request.data['documents']
            except Exception as e:
                logger.exception(f"documents не найден {e}")
                raise ValidationError("documents не найден", code=400)

            try:
                status = request.data['status']
            except Exception as e:
                logger.exception(f"status не найден {e}")
                raise ValidationError("status не найден", code=400)

            if get_current_new_status(Status, request).id != status:
                docs_req_types = document_type.objects.filter(
                    section=get_current_section(request), required=True
                ).values("id")
                docs_obj = [d['type'] for d in docs]
                for r in docs_req_types:
                    if r.get("id") not in docs_obj:
                        raise Exception("Отсутствует обязательный документ")
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator
