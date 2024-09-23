from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Request, Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .serializers import Meeting_app_serializer, Meeting_app_serializer_ff
from .models import Meeting_app
from .filter import Meeting_app_filter
from apps.constructor.services.applications import create_application, update_application, get_by_application_id
from .services.document import document_validation


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            # 'main_table_fields': get_main_table_fields_by_section_method(self.request),
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
        return q.filter(author=self.request.user.id)

    @swagger_auto_schema(request_body=Meeting_app_serializer_ff)
    def post(self, request, *args, **kwargs):
        document_validation(request)
        return create_application(request, Meeting_app_serializer)


class Application_detail(APIView):
    permission_classes = [IsAuthenticated]
    model_used = Meeting_app

    def get(self, request: Request, id: int):
        return get_by_application_id(request, id, Meeting_app, Meeting_app_serializer)

    @swagger_auto_schema(request_body=Meeting_app_serializer_ff)
    def put(self, request: Request, id: int):
        document_validation(request)
        return update_application(request, id, Meeting_app, Meeting_app_serializer)
