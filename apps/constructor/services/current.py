from rest_framework.views import Request
import logging

from apps.profiles.models import Profile, Roles
from apps.constructor.models import Contest, Schema, Status
from ..serializers import Schema_serializer
from users.models import CustomUser


logger = logging.getLogger('django')


def get_current_profile(request: Request) -> Profile:
    try:
        section = get_current_section(request)
        obj = Profile.objects.filter(user=request.user, section=section).last()
        return obj
    except Exception as e:
        logger.exception(f"Ошибка при поиске профиля пользователя {e}")
        raise Exception("Ошибка при поиске профиля пользователя")


def get_current_profile_type(request: Request):
    try:
        obj = Profile.objects.get(user=request.user).municipal_district.district_type
        return obj
    except Exception as e:
        logger.exception(f"Ошибка при поиске поля profile_type {e}")
        Exception("Ошибка при поиске поля profile_type")


def get_current_contest(request: Request) -> int:
    section = get_current_section(request)
    profile_type = get_current_profile_type(request).id
    contest = Contest.objects.filter(section=section, status='opened', district_type=profile_type)
    if contest.count() == 0:
        raise Exception("Конкурс с вашими критериями не найден")
    else:
        return contest.last()


def get_current_section(request: Request):
    obj = CustomUser.objects.get(id=request.user.id).current_section
    return obj


def get_current_schema(request: Request):
    try:
        section = get_current_section(request)
        obj = Schema.objects.get(section=section)
        return Schema_serializer(obj).data
    except Exception as e:
        logger.exception(f"Ошибка при поиске поля schema {e}")
        raise Exception("Ошибка при поиске поля schema")


def get_current_new_status(request: Request) -> Status:
    section = get_current_section(request)
    obj = Status.objects.get(section=section, title="Создана")
    return obj


def get_current_win_status(request: Request) -> Status:
    section = get_current_section(request)
    obj = Status.objects.get(section=section, title="Победила")
    return obj


def get_current_lose_status(request: Request) -> Status:
    section = get_current_section(request)
    obj = Status.objects.get(section=section, title="Проиграла")
    return obj


def get_current_moder_role() -> Roles:
    try:
        obj = Roles.objects.get(title="moderator")
        return obj
    except Exception:
        logger.exception("Ошибка при поиске роли Модератор")
        raise Exception("Ошибка при поиске роли Модератор")


def get_current_admin_role() -> Roles:
    try:
        obj = Roles.objects.get(title="admin")
        return obj
    except Exception:
        logger.exception("Ошибка при поиске роли Админ")
        raise Exception("Ошибка при поиске роли Админ")
