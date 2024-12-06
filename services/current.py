from rest_framework.views import Request
import logging
from django.db.models import Model
from django.apps import apps
from django.contrib.auth import get_user_model


logger = logging.getLogger('django')


def get_custom_user_model(app_name: str, model_name: str) -> Model:
    """
    Для избежания цикличности импортов
    """
    return apps.get_model(app_name, model_name)


def get_current_profile(request: Request):
    try:
        section = get_current_section(request)
        obj = get_custom_user_model('profiles', 'Profile').objects.filter(user=request.user, section=section).last()
        return obj
    except Exception as e:
        logger.exception(f"Ошибка при поиске профиля пользователя {e}")
        raise Exception("Ошибка при поиске профиля пользователя")


def get_current_profile_type(request: Request):
    try:
        section = get_current_section(request)
        obj = get_custom_user_model('profiles', 'Profile').objects.get(
            user=request.user, section=section
        ).district_type
        return obj
    except Exception as e:
        logger.exception(f"Ошибка при поиске поля profile_type {e}")
        Exception("Ошибка при поиске поля profile_type")


def get_current_contest(request: Request) -> int:
    section = get_current_section(request)
    profile_type = get_current_profile_type(request).id
    contest = get_custom_user_model(
        'constructor', 'Contest').objects.filter(section=section, status='opened', district_type=profile_type)
    if contest.count() == 0:
        logger.exception("Конкурс с вашими критериями не найден")
        raise Exception("Конкурс с вашими критериями не найден")
    else:
        return contest.last()


def get_current_section(request: Request):
    if request.user.is_authenticated:
        obj = get_user_model().objects.get(id=request.user.id).current_section
        return obj
    else:
        logger.exception("Пользователь не авторизован")
        raise Exception("Пользователь не авторизован")


def get_current_new_status(model: Model, request: Request):
    try:
        section = get_current_section(request)
        obj = model.objects.get(section=section, tech_name="new")
        return obj
    except Exception as e:
        logger.exception(f"Ошибка при поиске статуса 'new' {e}")
        raise Exception("Ошибка при поиске статуса 'new'")


def get_current_win_status(model: Model, request: Request):
    try:
        section = get_current_section(request)
        obj = model.objects.get(section=section, tech_name="win")
        return obj
    except Exception as e:
        logger.exception(f"Ошибка при поиске статуса 'win' {e}")
        raise Exception("Ошибка при поиске статуса 'win'")


def get_current_lose_status(model: Model, request: Request):
    try:
        section = get_current_section(request)
        obj = model.objects.get(section=section, tech_name="lose")
        return obj
    except Exception as e:
        logger.exception(f"Ошибка при поиске статуса 'lose' {e}")
        raise Exception("Ошибка при поиске статуса 'lose'")


def get_current_moder_role():
    try:
        obj = get_custom_user_model('profiles', 'Roles').objects.get(title="moderator")
        return obj
    except Exception:
        logger.exception("Ошибка при поиске роли Модератор")
        raise Exception("Ошибка при поиске роли Модератор")


def get_current_admin_role():
    try:
        obj = get_custom_user_model('profiles', 'Roles').objects.get(title="admin")
        return obj
    except Exception:
        logger.exception("Ошибка при поиске роли Админ")
        raise Exception("Ошибка при поиске роли Админ")
