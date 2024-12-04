from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (Application_serializer_ff, Document_type_serializer,
                          Status_serializer, Project_type_serializer_ff, Application_change_status_serializer,
                          Schema_serializer, Applications_serializer)
from .models import Application, Contest, Status, Project_type, Document_type, Schema
from services.decorators import Decorators
from .filter import Application_filter, Application_map_filter
from .services.applications import Application_services
from services.current import get_current_section
from .services.schema import get_schema_by_user
from apps.table_fields_manager.services import get_main_table_fields_by_section_method
from .services.status import Status_serives
from .services.project_type import (get_project_type_by_section, create_project_type, update_project_type,
                                    delete_project_type)
from .services.contest import create_contest, update_contest, get_contests_by_section, get_contest_by_year
from .services.decorators import application_number_validator, application_project_type_validator
from .services.document_type import Document_type_services
from .services.document import document_validation


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'main_table_fields': get_main_table_fields_by_section_method(self.request, Application),
            'total_results': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class Application_main(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Application.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = Application_filter
    model_used = Application

    def get_serializer_class(self):
        return Applications_serializer

    def get_queryset(self):
        q = self.filter_queryset(super().get_queryset())
        return Application_services.query_handler(self.request, q)

    @document_validation(Document_type)
    @Decorators.role_required_v2()
    @application_number_validator()
    @swagger_auto_schema(request_body=Application_serializer_ff)
    def post(self, request, *args, **kwargs):
        return Application_services.create_application(request)


class Application_detail(APIView):
    permission_classes = [IsAuthenticated]
    model_used = Application

    def get(self, request: Request, id: int):
        return Application_services.get_by_application_id(request, id)

    @document_validation(Document_type)
    @swagger_auto_schema(request_body=Application_serializer_ff)
    @Decorators.role_required_v2()
    @application_project_type_validator()
    def put(self, request: Request, id: int):
        return Application_services.update_application(request, id)


class Schema_main(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        return get_schema_by_user(request, Schema, Schema_serializer)


class Status_main(APIView):
    model_used = Status

    def get(self, request: Request):
        return Status_serives.get_all_statuses_by_section(request)

    @Decorators.role_required_v2()
    @swagger_auto_schema(request_body=Status_serializer)
    def post(self, request: Request):
        return Status_serives.create_status(request)


class Get_status_by_name(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
        ]
    )
    def get(self, request: Request):
        name = request.GET.get('name')
        return Status_serives.get_status_by_name(request, name)


class Status_detail(APIView):
    model_used = Status

    @swagger_auto_schema(request_body=Status_serializer)
    @Decorators.role_required_v2()
    def put(self, request: Request, id: int):
        return Status_serives.update_status(request, id)

    def delete(self, request: Request, id: int):
        return Status_serives.delete_status(request, id)


class Project_type_main(APIView):
    model_used = Project_type

    def get(self, request: Request):
        return get_project_type_by_section(request)

    @swagger_auto_schema(request_body=Project_type_serializer_ff)
    @Decorators.role_required_v2()
    def post(self, request: Request):
        return create_project_type(request)


class Project_type_detail(APIView):
    model_used = Project_type

    @swagger_auto_schema(request_body=Project_type_serializer_ff)
    @Decorators.role_required_v2()
    def put(self, request: Request, id: int):
        return update_project_type(request, id)

    def delete(self, request: Request, id: int):
        return delete_project_type(request, id)


class Contest_main(APIView):
    model_used = Contest

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('year', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False)
        ]
    )
    def get(self, request: Request):
        return get_contests_by_section(request)

    @Decorators.role_required_v2()
    def post(self, request: Request):
        return create_contest(request)


class Contest_detail(APIView):
    model_used = Contest

    @Decorators.role_required_v2()
    def put(self, request: Request, id: int):
        return update_contest(request, id)

    def get(self, request: Request, id: int):
        return get_contest_by_year(request, id)


class Document_type_main(APIView):
    model_used = Document_type

    def get(self, request: Request):
        return Document_type_services.get_all_document_types_by_section(request)

    @swagger_auto_schema(request_body=Document_type_serializer)
    def post(self, request: Request):
        return Document_type_services.create_document_type(request)


class Document_type_detail(APIView):
    model_used = Document_type

    @swagger_auto_schema(request_body=Document_type_serializer)
    def put(self, request: Request, id: int):
        return Document_type_services.update_document_type(request, id)

    def delete(self, request: Request, id: int):
        return Document_type_services.delete_document_type(request, id)


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
            return Application_services.application_for_map(queryset, request)
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)


class Application_change_status_to_win(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=Application_change_status_serializer)
    def post(self, request):
        contest_id = request.data.get("contest_id")
        return Application_services.change_applications_statuses_to_win(request, contest_id)
