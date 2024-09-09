from rest_framework.views import APIView, Response, Request
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from .services.profile_services import (get_profile, get_profile_by_user_id, update_user_data,
                                        update_profile_by_user_id, create_user)
from .serializers import User_serializer
from .services.role_handler import (create_role_handler, update_role_handler, get_all_roles_handler,
                                    delete_role_handler, get_role_handler_by_id, get_all_models)
from .services.role import (get_all_roles_by_section, create_role, update_role, delete_role)


class Profile_main(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(get_profile(request))

    @swagger_auto_schema(request_body=User_serializer)
    def put(self, request):
        return update_user_data(request)

    @swagger_auto_schema(request_body=User_serializer)
    def post(self, request):
        return create_user(request)


class Profile_detail(APIView):
    def get(self, request: Request, id: int):
        return Response(get_profile_by_user_id(id))

    @swagger_auto_schema(request_body=User_serializer)
    def put(self, request: Request, id: int):
        return update_profile_by_user_id(request, id)


class Role_handler_main(APIView):

    def get(self, request: Request):
        return get_all_roles_handler(request)

    def post(self, request: Request):
        return create_role_handler(request)


class Role_handler_detail(APIView):

    def get(self, request: Request, id: int):
        return get_role_handler_by_id(request, id)

    def put(self, request: Request, id: int):
        return update_role_handler(request, id)

    def delete(self, request: Request, id):
        return delete_role_handler(request, id)


class Model_main(APIView):
    def get(self, request: Request):
        return get_all_models(request)


class Role_main(APIView):
    def get(self, reqiest: Request):
        return get_all_roles_by_section(reqiest)

    def post(self, request: Request):
        return create_role(request)


class Role_detail(APIView):
    def put(self, request: Request, id: int):
        return update_role(request, id)

    def delete(self, request: Request, id: int):
        return delete_role(request, id)
