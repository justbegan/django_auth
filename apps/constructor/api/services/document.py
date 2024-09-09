from rest_framework.views import Request
from rest_framework.exceptions import ValidationError
import logging

from apps.constructor.classificators_models import Document_type
from .current import get_current_section, get_current_new_status

logger = logging.getLogger('django')


def document_validation(request: Request):
    """
    documents = [
        {
            "urls": [],
            "type": 1
        }
    ]
    """
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

    if get_current_new_status(request) != status:
        docs_req_types = Document_type.objects.filter(
            section=get_current_section(request), required=True
        ).values("id")
        docs_obj = [d['type'] for d in docs]
        for r in docs_req_types:
            if r.get("id") not in docs_obj:
                raise Exception("Отсутствует обязательный документ")
