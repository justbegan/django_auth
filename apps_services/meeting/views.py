from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .serializers import Meeting_app_serializer
from .models import Meeting_app
from .filter import Meeting_app_filter
from .services.current import get_current_contest, get_current_section
from .services.custom_data import validate_custom_data
from .services.document import document_validation
from .services.applications import get_by_meeting_application_id, update_meeting_application


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


class Meeting_application_main(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Meeting_app_serializer
    queryset = Meeting_app.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = Meeting_app_filter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user.id)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document_validation(request)
        serializer.save(
            custom_data=validate_custom_data(request),
            author=self.request.user,
            section=get_current_section(request),
            contest=get_current_contest(request)
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Meeting_application_detail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, id: int):
        return get_by_meeting_application_id(request, id)

    @swagger_auto_schema(request_body=Meeting_app_serializer)
    def put(self, request: Request, id: int):
        return update_meeting_application(request, id)
