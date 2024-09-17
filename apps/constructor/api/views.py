from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .serializers import (Applications_serializer, Application_update_serializer, Document_type_serializer,
                          Status_serializer)
from ..models import Application
from .filter import Application_filter, Application_map_filter
from .services.applications import get_by_application_id, update_application, win_lose_calculation, application_for_map
from .services.current import get_current_contest, get_current_section
from .services.schema import get_schema_by_user
from .services.custom_data import validate_custom_data
from .services.main_table_fields import get_main_table_fields_by_section, get_main_table_fields_by_section_method
from .services.status import get_all_statuses_by_section, create_status, update_status
from .services.project_type import get_project_type_by_section, create_project_type, update_project_type
from .services.contest import create_contest, update_contest, get_contests_by_section
from .services.document import document_validation
from .services.decorators import role_required_v2
from .services.document_type import create_document_type, update_document_type, get_all_document_types_by_section
from .services.custom_validation import custom_validation


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'main_table_fields': get_main_table_fields_by_section_method(self.request),
            'win_lose': win_lose_calculation(self.request, data),
            'total_results': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class Application_main(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Applications_serializer
    queryset = Application.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = Application_filter
    model_used = Application

    def get_queryset(self):
        q = super().get_queryset()
        return q.filter(author=self.request.user.id)

    @role_required_v2()
    def post(self, request, *args, **kwargs):
        request.data['author'] = self.request.user.id
        request.data['section'] = get_current_section(request).id
        request.data['contest'] = get_current_contest(request).id
        request.data['custom_data'] = validate_custom_data(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        custom_validation(request)
        document_validation(request)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Application_detail(APIView):
    permission_classes = [IsAuthenticated]
    model_used = Application

    def get(self, request: Request, id: int):
        return get_by_application_id(request, id)

    @swagger_auto_schema(request_body=Application_update_serializer)
    @role_required_v2()
    def put(self, request: Request, id: int):
        return update_application(request, id)


class Schema_main(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        return get_schema_by_user(request)


class Main_table_fields_main(APIView):
    def get(self, request: Request):
        return get_main_table_fields_by_section(request)


class Status_main(APIView):
    def get(self, request: Request):
        return get_all_statuses_by_section(request)

    @swagger_auto_schema(request_body=Status_serializer)
    def post(self, request: Request):
        return create_status(request)


class Status_detail(APIView):
    @swagger_auto_schema(request_body=Status_serializer)
    def put(self, request: Request, id: int):
        return update_status(request, id)


class Project_type_main(APIView):
    def get(self, request: Request):
        return get_project_type_by_section(request)

    @role_required_v2()
    def post(self, request: Request):
        return create_project_type(request)


class Project_type_detail(APIView):
    @role_required_v2()
    def put(self, request: Request, id: int):
        return update_project_type(request, id)


class Contest_main(APIView):
    def get(self, request: Request):
        return get_contests_by_section(request)

    @role_required_v2()
    def post(self, request: Request):
        return create_contest(request)


class Contest_detail(APIView):
    @role_required_v2()
    def put(self, request: Request, id: int):
        return update_contest(request, id)


class Document_type_main(APIView):
    def get(self, request: Request):
        return get_all_document_types_by_section(request)

    @swagger_auto_schema(request_body=Document_type_serializer)
    def post(self, request: Request):
        return create_document_type(request)


class Document_type_detail(APIView):
    @swagger_auto_schema(request_body=Document_type_serializer)
    def put(self, request: Request, id: int):
        return update_document_type(request, id)


class Application_for_map(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = Application_map_filter
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        section = get_current_section(request)
        queryset = Application.objects.filter(section=section)
        filterset = self.filterset_class(request.GET, queryset=queryset)

        if filterset.is_valid():
            queryset = filterset.qs
            print(queryset)
            return application_for_map(queryset, request)
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)
