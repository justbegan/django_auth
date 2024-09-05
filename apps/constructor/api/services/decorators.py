from functools import wraps
from rest_framework.response import Response
from rest_framework import status

from apps.profiles.models import Profile, Role_handler
from .current import get_current_section


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


def role_required_v2(end_point_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            user_role = Profile.objects.get(user=request.user).role

            method_roles = Role_handler.objects.get(
                section=get_current_section(request),
                end_point_name=end_point_name
            )
            if user_role not in method_roles.roles.all():
                return Response(
                    {"detail": "У вас нет прав для создания записи."},
                    status=status.HTTP_403_FORBIDDEN
                )

            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator
