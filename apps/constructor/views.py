from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .serializers import (Applications_serializer, Application_serializer_ff, Document_type_serializer,
                          Status_serializer, Project_type_serializer_ff)
from .models import Application, Contest, Status, Project_type, Document_type
from .filter import Application_filter, Application_map_filter
from .services.applications import (get_by_application_id, update_application, win_lose_calculation,
                                    application_for_map, create_application)
from .services.current import get_current_section, get_current_profile
from .services.schema import get_schema_by_user
from apps.table_fields_manager.services import get_main_table_fields_by_section_method
from .services.status import get_all_statuses_by_section, create_status, update_status, delete_status
from .services.project_type import (get_project_type_by_section, create_project_type, update_project_type,
                                    delete_project_type)
from .services.contest import create_contest, update_contest, get_contests_by_section, get_contest_by_year
from .services.decorators import role_required_v2
from .services.document_type import (create_document_type, update_document_type, get_all_document_types_by_section,
                                     delete_document_type)
from .services.document import document_validation


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'main_table_fields': get_main_table_fields_by_section_method(self.request, Application),
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
        return q.filter(author=get_current_profile(self.request))

    @document_validation(Document_type)
    @role_required_v2()
    @swagger_auto_schema(request_body=Application_serializer_ff)
    def post(self, request, *args, **kwargs):
        return create_application(request, Applications_serializer)


class Application_detail(APIView):
    permission_classes = [IsAuthenticated]
    model_used = Application

    def get(self, request: Request, id: int):
        return get_by_application_id(request, id, Application, Applications_serializer)

    @document_validation(Document_type)
    @swagger_auto_schema(request_body=Application_serializer_ff)
    @role_required_v2()
    def put(self, request: Request, id: int):
        return update_application(request, id, Application, Applications_serializer)


class Schema_main(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        return get_schema_by_user(request)


class Status_main(APIView):
    model_used = Status

    def get(self, request: Request):
        return get_all_statuses_by_section(request)

    @role_required_v2()
    @swagger_auto_schema(request_body=Status_serializer)
    def post(self, request: Request):
        return create_status(request)


class Status_detail(APIView):
    model_used = Status

    @swagger_auto_schema(request_body=Status_serializer)
    @role_required_v2()
    def put(self, request: Request, id: int):
        return update_status(request, id)

    def delete(self, request: Request, id: int):
        return delete_status(request, id)


class Project_type_main(APIView):
    model_used = Project_type

    def get(self, request: Request):
        return get_project_type_by_section(request)

    @swagger_auto_schema(request_body=Project_type_serializer_ff)
    @role_required_v2()
    def post(self, request: Request):
        return create_project_type(request)


class Project_type_detail(APIView):
    model_used = Project_type

    @swagger_auto_schema(request_body=Project_type_serializer_ff)
    @role_required_v2()
    def put(self, request: Request, id: int):
        return update_project_type(request, id)

    def delete(self, request: Request, id: int):
        return delete_project_type(request, id)


class Contest_main(APIView):
    model_used = Contest

    def get(self, request: Request):
        return get_contests_by_section(request)

    @role_required_v2()
    def post(self, request: Request):
        return create_contest(request)


class Contest_detail(APIView):
    model_used = Contest

    @role_required_v2()
    def put(self, request: Request, id: int):
        return update_contest(request, id)

    def get(self, request: Request, id: int):
        return get_contest_by_year(request, id)


class Document_type_main(APIView):
    model_used = Document_type

    def get(self, request: Request):
        return get_all_document_types_by_section(request)

    @swagger_auto_schema(request_body=Document_type_serializer)
    def post(self, request: Request):
        return create_document_type(request)


class Document_type_detail(APIView):
    model_used = Document_type

    @swagger_auto_schema(request_body=Document_type_serializer)
    def put(self, request: Request, id: int):
        return update_document_type(request, id)

    def delete(self, request: Request, id: int):
        return delete_document_type(request, id)


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
            return application_for_map(queryset, request)
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)
