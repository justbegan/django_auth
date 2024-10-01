from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Request, Response
from rest_framework import status
from .serializers import VerifyCodeSerializer

from .services import get_user, get_user_id, update_user, create_user, repeat_email, recover_password
from .serializers import User_serializer, Repeat_email_ff, Recover_password_ff, User_serializer_ff
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
    serializer_class = User_serializer
    queryset = CustomUser.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = Custom_user_filter

    def get_queryset(self):
        return super().get_queryset()

    @swagger_auto_schema(request_body=User_serializer_ff)
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


class Verify_code(generics.GenericAPIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Учетная запись успешно активирована!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Repeat_email(APIView):
    @swagger_auto_schema(request_body=Repeat_email_ff)
    def post(self, request):
        return repeat_email(request)


class Recover_password(APIView):
    @swagger_auto_schema(request_body=Recover_password_ff)
    def post(self, request: Request):
        return recover_password(request)
