from functools import wraps
from rest_framework.response import Response
from rest_framework import status

from apps.profiles.models import Role_handler
from services.current import get_current_section, get_current_profile, get_current_contest
import logging
from django.contrib.contenttypes.models import ContentType
from ..models import Application, Status


logger = logging.getLogger('django')


def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            user_role = get_current_profile(request).role.title
            if user_role not in allowed_roles:
                return Response(
                    {"message": "У вас нет прав для создания записи."},
                    status=status.HTTP_403_FORBIDDEN
                )
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator


def role_required_v2():
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if request.method == 'POST':
                error_text = "У вас нет прав для создания записи."
            else:
                error_text = "У вас нет прав для изменения записи."
            user_role = get_current_profile(request).role
            used_model_content_type = ContentType.objects.get_for_model(self.model_used)
            try:
                method_roles = Role_handler.objects.get(
                    section=get_current_section(request),
                    model=used_model_content_type
                )
                if not method_roles.roles.filter(id=user_role.id):
                    return Response(
                        {"message": error_text},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Exception as e:
                logger.exception(f"Не могу найти роль метода {e}")
                return Response(
                    {"message": error_text},
                    status=status.HTTP_403_FORBIDDEN
                )

            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator


def application_number_validator():
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            current_profile = get_current_profile(request)
            user_allowed_number = current_profile.allowed_number_projects
            application_number = Application.objects.filter(
                author=current_profile, contest=get_current_contest(request)
            ).count()
            if application_number >= user_allowed_number:
                return Response(
                    {"message": "У вас максимальное колличестов заявок!"},
                    status=status.HTTP_403_FORBIDDEN
                )
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator


def application_project_type_validator():
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            project_type = request.data.get('project_type', None)
            if project_type is None:
                return Response(
                    {"message": "Поле 'Типология проекта' не может быть пустым"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator


def status_validator():
    def decorator(func):
        @wraps(func)
        def wrapper(cls, request, *args, **kwargs):
            if cls.status:
                app_status: Status = cls.status.objects.get(id=request.data.get('status'))
                if app_status.roles.all().count() > 0:
                    user_role = get_current_profile(request).role
                    if app_status.roles.filter(id=user_role.id).count() == 0:
                        return Response(
                            {"message": "У вас нет права на этот статус"},
                            status=status.HTTP_403_FORBIDDEN
                        )
            return func(cls, request, *args, **kwargs)
        return wrapper
    return decorator
