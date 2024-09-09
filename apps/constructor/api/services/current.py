from rest_framework.views import Request
import logging

from apps.profiles.models import Profile
from apps.constructor.models import Contest, Schema, Status
from ..serializers import Schema_serializer


logger = logging.getLogger('django')


def get_current_profile_type(request: Request):
    try:
        return Profile.objects.get(user=request.user).profile_type
    except Exception as e:
        logger.exception(f"Ошибка при поиске поля profile_type {e}")
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
        return Profile.objects.get(user=request.user).section
    except Exception as e:
        logger.exception(f"Ошибка при поиске поля profile section {e}")
        raise Exception("Ошибка при поиске поля profile section")


def get_current_schema(request: Request):
    try:
        section = get_current_section(request)
        obj = Schema.objects.get(section=section)
        return Schema_serializer(obj).data
    except Exception as e:
        logger.exception(f"Ошибка при поиске поля schema {e}")
        raise Exception("Ошибка при поиске поля schema")


def get_current_new_status(request: Request) -> int:
    try:
        section = get_current_section(request)
        obj = Status.objects.get(section=section, title="Создана").id
        return obj
    except Exception as e:
        logger.exception(f"Не могу найти статус с именем 'Создана' {e}")
        raise Exception("Не могу найти статус с именем 'Создана'")
