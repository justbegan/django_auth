from rest_framework.views import APIView, Request
from drf_yasg.utils import swagger_auto_schema

from .services import create_letter, update_letter, delete_letter, get_all_letters_by_section
from .serializers import Letter_serializer_ff


class Letter_main(APIView):
    @swagger_auto_schema(request_body=Letter_serializer_ff)
    def post(self, request: Request):
        return create_letter(request)

    def get(self, request: Request):
        return get_all_letters_by_section(request)


class Letter_detail(APIView):
    @swagger_auto_schema(request_body=Letter_serializer_ff)
    def put(self, request: Request, id: int):
        return update_letter(request, id)

    def delete(self, request: Request, id: int):
        return delete_letter(request, id)
