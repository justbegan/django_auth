from rest_framework.views import APIView, Request
from drf_yasg.utils import swagger_auto_schema

from .services import News_services
from .serializers import News_serializer_ff
from services.decorators import Decorators
from .models import News


class News_main(APIView):
    model_used = News

    def get(self, request: Request):
        """
        Получить все новости
        """
        return News_services.get_all_news(request)

    @Decorators.role_required_v2()
    @swagger_auto_schema(request_body=News_serializer_ff)
    def post(self, request: Request):
        return News_services.create_news(request)


class News_detail(APIView):
    model_used = News

    def get(self, request: Request, id: int):
        return News_services.get_new_by_id(request, id)

    @Decorators.role_required_v2()
    @swagger_auto_schema(request_body=News_serializer_ff)
    def put(self, request: Request, id: int):
        return News_services.update_news(request, id)

    @Decorators.role_required_v2()
    def delete(self, request: Request, id: int):
        return News_services.delete_news(request, id)
