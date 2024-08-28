from rest_framework.views import Request
from apps.profiles.models import Profile
from apps.constructor.models import Contest, Schema, Status
from ..serializers import Schema_serializer


def get_current_contest(request: Request) -> int:
    try:
        section = get_current_section(request)
        return Contest.objects.get(section=section)
    except:
        raise Exception("contest is not selected")


def get_current_section(request: Request):
    return Profile.objects.get(user=request.user).section


def get_current_schema(request: Request):
    try:
        section = get_current_section(request)
        obj = Schema.objects.get(section=section)
        return Schema_serializer(obj).data
    except:
        raise Exception("schema is not selected")


def get_current_new_status(request: Request):
    try:
        section = get_current_section(request)
        obj = Status.objects.get(section=section, title="Создана").id
        return obj
    except:
        raise Exception("created status is not found")
