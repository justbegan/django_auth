from rest_framework.views import Request, APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from .services import (get_all_question_by_section, create_question, update_question, delete_question)
from .serializer import Question_serializer


class Question_main(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        return get_all_question_by_section(request)

    @swagger_auto_schema(request_body=Question_serializer)
    def post(self, request: Request):
        return create_question(request)


class Question_detail(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=Question_serializer)
    def put(self, request: Request, id: int):
        return update_question(request, id)

    def delete(self, request: Request):
        return delete_question(request, id)
