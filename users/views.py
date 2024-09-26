from rest_framework.views import Request, APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .services import get_user, get_user_id, update_user, create_user, get_all_users, get_new_users
from .serializers import User_serializer_ff, User_serializer


class Users_main(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'get_all',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description='Filter by active status',
                required=False
            )
        ]
    )
    def get(self, request: Request):
        get_all = request.query_params.get('get_all', 'true')
        if get_all == 'true':
            return get_all_users(request)
        else:
            return get_new_users(request)

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
