from functools import wraps
from rest_framework.views import Response, Request
from rest_framework import status

from apps.profiles.models import Role_handler
from .current import get_current_section, get_current_profile
import logging
from django.contrib.contenttypes.models import ContentType


logger = logging.getLogger('django')


class Decorators:
    @staticmethod
    def role_required_v2():
        def decorator(func):
            @wraps(func)
            def wrapper(self, request: Request, *args, **kwargs):
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
