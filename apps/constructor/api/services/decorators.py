from functools import wraps
from rest_framework.response import Response
from rest_framework import status

from apps.profiles.models import Profile, Role_handler
from .current import get_current_section
import logging
from django.contrib.contenttypes.models import ContentType


logger = logging.getLogger('django')


def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            user_role = Profile.objects.get(user=request.user).role.title
            if user_role not in allowed_roles:
                return Response(
                    {"detail": "У вас нет прав для создания записи."},
                    status=status.HTTP_403_FORBIDDEN
                )
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator


def role_required_v2():
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            user_role = Profile.objects.get(user=request.user).role
            used_model_content_type = ContentType.objects.get_for_model(self.model_used)
            try:
                method_roles = Role_handler.objects.get(
                    section=get_current_section(request),
                    model=used_model_content_type
                )
                if user_role not in method_roles.roles.all():
                    return Response(
                        {"detail": "У вас нет прав для создания записи."},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Exception as e:
                logger.exception(f"Не могу найти роль метода {e}")

            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator
