from rest_framework.views import Request, Response

from .models import News
from .serializers import News_serializer
from services.crud import get_many, create, update, delete, get


def get_all_news(request: Request):
    return Response(get_many(News, News_serializer, {"hide": False}, "-id"))


def create_news(request: Request):
    return Response(create(News_serializer, request.data))


def update_news(request: Request, id: int):
    return Response(update(News, News_serializer, request.data, {"id": id}))


def get_new_by_id(request: Request, id: int):
    return Response(get(News, News_serializer, {"id": id, "hide": False}))


def delete_news(request: Request, id: int):
    return Response(delete(News, {"id": id}))
