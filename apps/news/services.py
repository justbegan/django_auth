from rest_framework.views import Request, Response
from copy import deepcopy

from .models import News
from .serializers import News_serializer
from services.crud_services import Base_crud
from services.current import get_current_section


class News_services:
    @staticmethod
    def get_all_news(request: Request):
        return Response(
            Base_crud.get_many(News, News_serializer, {"hide": False, "section": get_current_section(request)}, "-id")
        )

    @staticmethod
    def create_news(request: Request):
        data = deepcopy(request.data)
        data['section'] = get_current_section(request).id
        return Response(Base_crud.create(News_serializer, data))

    @staticmethod
    def update_news(request: Request, id: int):
        data = deepcopy(request.data)
        data['section'] = get_current_section(request).id
        return Response(Base_crud.update(News, News_serializer, data, {"id": id}))

    @staticmethod
    def get_new_by_id(request: Request, id: int):
        return Response(Base_crud.get(News, News_serializer, {"id": id, "hide": False}))

    @staticmethod
    def delete_news(request: Request, id: int):
        return Response(Base_crud.delete(News, {"id": id}))
