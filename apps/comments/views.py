from rest_framework.views import APIView, Request
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from .services import create_comments, get_comments_by_application_id
from .serializers import Comments_serializer


class Comment_main(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=Comments_serializer)
    def post(self, request: Request):
        return create_comments(request)


class Comment_detail(APIView):
    """
    Получить все комменты по id заявки
    """
    def get(self, request: Request, id: int):
        return get_comments_by_application_id(request, id)
