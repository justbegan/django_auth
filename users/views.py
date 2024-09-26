from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Request, Response
from rest_framework.permissions import IsAuthenticated

from .services import get_user, get_user_id, update_user, create_user
from .serializers import User_serializer
from users.models import CustomUser
from .filters import Custom_user_filter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'total_results': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class Users_main(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = User_serializer
    queryset = CustomUser.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = Custom_user_filter

    def get_queryset(self):
        return super().get_queryset()

    def post(self, request, *args, **kwargs):
        return create_user(request)


class Users_detail(APIView):
    def get(self, request: Request, id: int):
        return get_user_id(request, id)

    @swagger_auto_schema(request_body=User_serializer)
    def put(self, request: Request, id: int):
        return update_user(request, id)


class Current_user(APIView):
    def get(self, request: Request):
        return get_user(request)
