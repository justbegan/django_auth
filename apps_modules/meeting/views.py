from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Request, Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .serializers import (Meeting_app_serializer, Meeting_app_serializer_ff, Meeting_schema_serializer)
from .models import Meeting_app, Meeting_document_type, Meeting_schema, Status
from .filter import Meeting_app_filter
from .services.meeting import Meeting_services
from apps.constructor.services.schema import get_schema_by_user
from apps.constructor.services.document import document_validation
from apps.table_fields_manager.services import get_main_table_fields_by_section_method
from .services.document_type import Document_type_services
from .services.status import Meeting_status_services
from services.current import get_current_profile, get_current_section
from services.decorators import Decorators


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'main_table_fields': get_main_table_fields_by_section_method(self.request, Meeting_app),
            'total_results': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class Application_main(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Meeting_app_serializer
    queryset = Meeting_app.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = Meeting_app_filter
    model_used = Meeting_app

    def get_queryset(self):
        q = super().get_queryset()
        condition = [
            get_current_profile(self.request).role.title == 'moderator',
            get_current_profile(self.request).role.title == 'admin'
        ]
        if any(condition):
            return q.filter(contest__section=get_current_section(self.request)).order_by('-created_at')
        else:
            return q.filter(author=get_current_profile(self.request)).order_by('-created_at')

    @Decorators.role_required_v2()
    @document_validation(Meeting_document_type)
    @swagger_auto_schema(request_body=Meeting_app_serializer_ff)
    def post(self, request, *args, **kwargs):
        return Meeting_services.create_application(request)


class Application_detail(APIView):
    permission_classes = [IsAuthenticated]
    model_used = Meeting_app

    def get(self, request: Request, id: int):
        return Meeting_services.get_by_application_id(request, id)

    @Decorators.role_required_v2()
    @document_validation(Meeting_document_type)
    @swagger_auto_schema(request_body=Meeting_app_serializer_ff)
    def put(self, request: Request, id: int):
        return Meeting_services.update_application(request, id)


class Schema_main(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        return get_schema_by_user(request, Meeting_schema, Meeting_schema_serializer)


class Document_type_main(APIView):
    model_used = Meeting_document_type

    def get(self, request: Request):
        return Document_type_services.get_all_document_types_by_section(request)


class Status_main(APIView):
    model_used = Status

    def get(self, request: Request):
        return Meeting_status_services.get_all_statuses_by_section(request)


class Create_application_by_meeting_id(APIView):
    @Decorators.role_required_v2()
    def post(self, request: Request, meeting_id: int):
        return Meeting_services.create_app(request, meeting_id)
