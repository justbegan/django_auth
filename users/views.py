from rest_framework.views import Request, APIView
from drf_yasg.utils import swagger_auto_schema

from .services import get_user, get_user_id, update_user, create_user, get_all_users
from .serializers import User_serializer_ff, User_serializer


class Users_main(APIView):
    def get(self, request: Request):
        return get_all_users(request)

    @swagger_auto_schema(request_body=User_serializer_ff)
    def post(self, request: Request):
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
