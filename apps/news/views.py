from rest_framework.views import APIView, Request
from drf_yasg.utils import swagger_auto_schema

from .services import get_all_news, create_news, update_news, delete_news, get_new_by_id
from .serializers import News_serializer_ff
from services.decorators import Decorators


class News_main(APIView):
    def get(self, request: Request):
        """
        Получить все новости
        """
        return get_all_news(request)

    @Decorators.role_required_v2()
    @swagger_auto_schema(request_body=News_serializer_ff)
    def post(self, request: Request):
        return create_news(request)


class News_detail(APIView):
    def get(self, request: Request, id: int):
        return get_new_by_id(request, id)

    @Decorators.role_required_v2()
    @swagger_auto_schema(request_body=News_serializer_ff)
    def put(self, request: Request, id: int):
        return update_news(request, id)

    @Decorators.role_required_v2()
    def delete(self, request: Request, id: int):
        return delete_news(request, id)
