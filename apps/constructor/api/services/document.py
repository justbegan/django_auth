from rest_framework.views import Request

from apps.constructor.classificators_models import Document_type
from .current import get_current_section, get_current_new_status


def document_validation(request: Request):
    # documents = [1, 2, 3]
    docs = request.data['documents']
    status = request.data['status']
    if get_current_new_status(request) != status:
        docs_req_types = Document_type.objects.filter(
            section=get_current_section(request), required=True
        ).values_list('id')
        docs_obj = [d['type'] for d in docs]
        for r in docs_req_types:
            if r not in docs_obj:
                raise Exception("Отсутствует обязательный документ")
