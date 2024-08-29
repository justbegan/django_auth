from rest_framework.views import Response, Request
from django.db import models

from apps.constructor import classificators_models as app_models
from .current import get_current_section


def get_all_classificators(request: Request) -> Response:
    result = {}
    for name, obj in vars(app_models).items():
        if isinstance(obj, type) and issubclass(obj, models.Model):
            try:
                result[name] = obj.objects.filter(section=get_current_section(request)).values()
            except:
                pass

    return Response(result)
