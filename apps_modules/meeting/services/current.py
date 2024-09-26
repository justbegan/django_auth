from rest_framework.views import Request

from ..models import Meeting_schema, Status
from apps.constructor.models import Contest
from ..serializers import Meetign_schema_serializer


def get_current_profile_type(request: Request):
    try:
        return request.user.profile.profile_type
    except Exception:
        Exception("Ошибка при поиске поля profile_type")


def get_current_contest(request: Request) -> int:
    section = get_current_section(request)
    profile_type = get_current_profile_type(request).id
    contest = Contest.objects.filter(section=section, status='opened', contest_types=profile_type)
    if contest.count() == 0:
        raise Exception("Конкурс с вашими критериями не найден")
    else:
        return contest.last()


def get_current_section(request: Request):
    try:
        return request.user.profile.section
    except Exception:
        raise Exception("Ошибка при поиске поля profile section")


def get_current_schema(request: Request):
    try:
        section = get_current_section(request)
        obj = Meeting_schema.objects.get(section=section)
        return Meetign_schema_serializer(obj).data
    except Exception:
        raise Exception("Ошибка при поиске поля schema")


def get_current_new_status(request: Request) -> int:
    try:
        section = get_current_section(request)
        obj = Status.objects.get(section=section, title="Создан").id
        return obj
    except Exception:
        raise Exception("Не могу найти статус с именем 'Создан'")
