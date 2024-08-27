from rest_framework.views import Response, Request

from ..serializers import Comments_serializer
from apps.constructor.models import Comments, Application
from .crud import create, get_many


def create_comments(request: Request):
    data = request.data.copy()
    data['author'] = request.user.id
    return Response(create(Comments_serializer, data))


def get_comments_by_application_id(request: Request, app_id: int):
    application = Application.objects.get(id=app_id)
    return Response(get_many(Comments, Comments_serializer, {"application": application}))
