from rest_framework.views import Response, Request
from django.core.mail import send_mail
from django.conf import settings
from functools import wraps
import logging

from django.contrib.contenttypes.models import ContentType
from services.crud import create, get_many
from .serializers import Comments_serializer
from .models import Comments
from apps.constructor.models import Application
from apps.profiles.models import Profile
from apps.constructor.services.current import get_current_section, get_current_moder_role


logger = logging.getLogger('django')


def send_email_decorator():
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            content_type_id = request.data.get("content_type", None)
            if content_type_id is None or content_type_id == 16:
                send_email_for_app_comment(request)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


@send_email_decorator()
def create_comments(request: Request):
    data = request.data.copy()
    data['author'] = request.user.id
    data['content_type'] = data.get("content_type", 16)
    return Response(create(Comments_serializer, data))


def get_comments_by_application_id(request: Request, app_id: int):
    application_content_type = ContentType.objects.get(model='application')
    return Response(get_many(Comments, Comments_serializer, {
        "object_id": app_id, "content_type": application_content_type
    }))


def create_comment_and_change_status(request: Request, data: dict, app_id: int) -> bool:
    APLICATION_CONTENT_TYPE_ID = 16
    data['author'] = request.user.id
    data['content_type'] = data.get("content_type", APLICATION_CONTENT_TYPE_ID)
    data['object_id'] = app_id
    return Response(create(Comments_serializer, data))


def send_email_for_app_comment(request: Request):
    try:
        moders_mail_list = [p.user.email for p in Profile.objects.filter(
            section=get_current_section(request), role=get_current_moder_role())
        ]
        if Profile.objects.get(user__id=request.user.id).role == get_current_moder_role():
            app_id = request.data.get('object_id', None)
            if app_id is not None:
                raise Exception("object_id is not found")
            user_email = Application.objects.get(id=app_id).author.user.email
            recipient = [user_email]
        else:
            recipient = moders_mail_list
    except Exception as e:
        logger.exception(e)
        raise Exception(e)
    send_mail(
        f'Новый комментарий от пользователя {request.user.username}',
        f'{request.data["text"]}',
        settings.DEFAULT_FROM_EMAIL,
        recipient,
        fail_silently=False,
    )
