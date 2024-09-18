from rest_framework.views import Request, APIView
from drf_yasg.utils import swagger_auto_schema

from .services import get_phone_books_by_section, create_phone_book, update_phone_book, delete_phone_book
from .serializers import Phone_book_serializer_for_swagger


class Phone_book_main(APIView):
    def get(self, request: Request):
        return get_phone_books_by_section(request)

    @swagger_auto_schema(request_body=Phone_book_serializer_for_swagger)
    def post(self, request: Request):
        return create_phone_book(request)


class Phone_book_details(APIView):
    @swagger_auto_schema(request_body=Phone_book_serializer_for_swagger)
    def put(self, request: Request, id: int):
        return update_phone_book(request, id)

    def delete(self, request: Request, id: int):
        return delete_phone_book(request, id)
