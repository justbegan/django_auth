from rest_framework.views import Response, Request
from django.db import models
import logging

from apps.constructor import classificators_models as app_models
from .current import get_current_section

logger = logging.getLogger('django')


def get_all_classificators(request: Request) -> Response:
    result = {}
    for name, obj in vars(app_models).items():
        if isinstance(obj, type) and issubclass(obj, models.Model):
            try:
                result[name.lower()] = obj.objects.filter(section=get_current_section(request)).values()
            except Exception as e:
                logging.exception(f"Ошибка при формировании классификторов {e}")
                pass

    return Response(result)
