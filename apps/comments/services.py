from rest_framework.views import Response, Request
from rest_framework.validators import ValidationError

from django.contrib.contenttypes.models import ContentType
from apps.constructor.api.services.crud import create, get_many
from apps.constructor.models import Application
from .serializers import Comments_serializer
from .models import Comments


def create_comments(request: Request):
    model_name = request.GET.get("type", "application")
    application_content_type = ContentType.objects.get(model=model_name)
    data = request.data.copy()
    data['author'] = request.user.id
    data['content_type'] = application_content_type.id
    return Response(create(Comments_serializer, data))


def get_comments_by_application_id(request: Request, app_id: int):
    application_content_type = ContentType.objects.get(model='application')
    return Response(get_many(Comments, Comments_serializer, {
        "object_id": app_id, "content_type": application_content_type
    }))


def create_comment_and_change_status(request: Request):
    model_name = request.GET.get("type", "application")
    application_content_type = ContentType.objects.get(model=model_name)
    data = request.data.copy()
    data['author'] = request.user.id
    data['content_type'] = application_content_type.id
    try:
        status = data["status"]
    except Exception:
        raise ValidationError("Поле status не найдено")
    Application.objects.filter(id=data["object_id"]).update(status=status)
    return Response(create(Comments_serializer, data))
