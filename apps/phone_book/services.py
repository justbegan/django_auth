from rest_framework.views import Request, Response
from copy import deepcopy
from services.crud import create, update, delete, get_many

from services.current import get_current_section
from .serializers import Phone_book_serializer
from .models import Phone_book


class Phone_book_services:
    @staticmethod
    def create_phone_book(request: Request):
        data = deepcopy(request.data)
        data['section'] = get_current_section(request).id
        return Response(create(Phone_book_serializer, data))

    @staticmethod
    def update_phone_book(request: Request, pk: int):
        data = deepcopy(request.data)
        data['section'] = get_current_section(request).id
        return Response(update(Phone_book, Phone_book_serializer, data, {'id': pk}))

    @staticmethod
    def get_phone_books_by_section(request: Request):
        return Response(get_many(Phone_book, Phone_book_serializer, {'section': get_current_section(request)}))

    @staticmethod
    def delete_phone_book(request: Request, pk: int):
        return Response(delete(Phone_book, {'id': pk}))
