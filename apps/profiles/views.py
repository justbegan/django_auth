from rest_framework.views import APIView, Request, Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import Section_serializer_ff, Profile_serializer
from .services.role_handler import (create_role_handler, update_role_handler, get_all_roles_handler,
                                    delete_role_handler, get_role_handler_by_id, get_all_models)
from .services.role import (get_all_roles_by_section, create_role, update_role, delete_role)
from .services.section import (get_all_sections, create_section, update_section, get_section_by_id,
                               get_sections_by_user)
from .services.profile_type import get_all_profile_types
from .models import Profile
from .filters import Profile_filter
from apps.constructor.services.current import get_current_section


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


class Profile_main(generics.ListAPIView):
    serializer_class = Profile_serializer
    queryset = Profile.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = Profile_filter

    def get_queryset(self):
        return super().get_queryset().filter(section=get_current_section(self.request))


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
