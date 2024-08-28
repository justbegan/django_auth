from rest_framework.views import Request, Response

from .models import News
from .serializers import News_serializer
from apps.constructor.api.services.crud import get_many, create, update, delete


def get_all_news(request: Request):
    return Response(get_many(News, News_serializer))


def create_news(request: Request):
    return Response(create(News_serializer, request.data))


def update_news(request: Request, id: int):
    return Response(update(News, News_serializer, request.data, {"id": id}))


def delete_news(request: Request, id: int):
    return Response(delete(News, {"id": id}))
