from rest_framework.views import Request
from rest_framework.validators import ValidationError

from apps.constructor.models import Application, Custom_validation
from .current import get_current_section, get_current_contest
from apps.profiles.models import Profile


def custom_validation(request: Request):
    try:
        custom_validation_code = Custom_validation.objects.get(section=get_current_section(request)).code
    except Exception:
        custom_validation_code = None

    if custom_validation_code:
        exec(custom_validation_code)
