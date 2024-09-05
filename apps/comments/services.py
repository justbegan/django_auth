from rest_framework.views import Response, Request

from django.contrib.contenttypes.models import ContentType
from apps.constructor.api.services.crud import create, get_many
from .serializers import Comments_serializer
from .models import Comments


def create_comments(request: Request):
    application_content_type = ContentType.objects.get(model='application')
    data = request.data.copy()
    data['author'] = request.user.id
    data['object_id'] = data['application']
    data['content_type'] = application_content_type.id
    return Response(create(Comments_serializer, data))


def get_comments_by_application_id(request: Request, app_id: int):
    application_content_type = ContentType.objects.get(model='application')
    return Response(get_many(Comments, Comments_serializer, {
        "object_id": app_id, "content_type": application_content_type
    }))
