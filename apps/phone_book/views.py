from rest_framework.views import Request, APIView
from drf_yasg.utils import swagger_auto_schema

from .services import Phone_book_services
from .serializers import Phone_book_serializer_ff
from services.decorators import Decorators
from .models import Phone_book


class Phone_book_main(APIView):
    model_used = Phone_book

    def get(self, request: Request):
        return Phone_book_services.get_phone_books_by_section(request)

    @Decorators.role_required_v2()
    @swagger_auto_schema(request_body=Phone_book_serializer_ff)
    def post(self, request: Request):
        return Phone_book_services.create_phone_book(request)


class Phone_book_details(APIView):
    model_used = Phone_book

    @Decorators.role_required_v2()
    @swagger_auto_schema(request_body=Phone_book_serializer_ff)
    def put(self, request: Request, id: int):
        return Phone_book_services.update_phone_book(request, id)

    @Decorators.role_required_v2()
    def delete(self, request: Request, id: int):
        return Phone_book_services.delete_phone_book(request, id)
