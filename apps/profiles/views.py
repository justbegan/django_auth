from rest_framework.views import APIView, Request
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import Section_serializer_ff
from .services.role_handler import (create_role_handler, update_role_handler, get_all_roles_handler,
                                    delete_role_handler, get_role_handler_by_id, get_all_models)
from .services.role import (get_all_roles_by_section, create_role, update_role, delete_role)
from .services.section import (get_all_sections, create_section, update_section, get_section_by_id,
                               get_sections_by_user)
from .services.profile_type import get_all_profile_types


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


class Section_main(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'get_all', openapi.IN_QUERY,
                description="Flag to retrieve all sections (0 or 1)",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request: Request):
        get_all = int(request.GET.get('get_all', True))
        if get_all:
            return get_all_sections(request)
        else:
            return get_sections_by_user(request)

    @swagger_auto_schema(request_body=Section_serializer_ff)
    def post(self, request: Request):
        return create_section(request)


class Section_detail(APIView):
    def get(self, request: Request, id: int):
        return get_section_by_id(request, id)

    @swagger_auto_schema(request_body=Section_serializer_ff)
    def put(self, request: Request, id: int):
        return update_section(request, id)


class Profile_type_main(APIView):
    def get(self, request: Request):
        return get_all_profile_types(request)
