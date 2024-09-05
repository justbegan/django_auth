from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .serializers import Applications_serializer
from ..models import Application
from .filter import Application_filter
from .services.classificators import get_all_classificators
from .services.applications import get_by_application_id, update_application, win_lose_calculation
from .services.current import get_current_contest, get_current_section
from .services.schema import get_schema_by_user
from .services.custom_data import validate_custom_data
from apps.history.services import create_history
from .services.main_table_fields import get_main_table_fields_by_section, get_main_table_fields_by_section_method
from .services.status import get_all_statuses_by_section
from .services.project_type import get_project_type_by_section, create_project_type, update_project_type
from .services.contest import create_contest, update_contest, get_contests_by_section
from .services.document import document_validation
from .services.decorators import role_required
from .services.decorators import role_required_v2


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'main_table_fields': get_main_table_fields_by_section_method(self.request),
            'win_lose': win_lose_calculation(self.request),
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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user.id)

    @role_required_v2("applications")
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
        history_data = {
            "author": request.user.id,
            "text": "Заявка создана",
            "application": serializer.data["id"]
        }
        try:
            create_history(history_data)
        except Exception as e:
            print(e)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Application_detail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, id: int):
        return get_by_application_id(request, id)

    @swagger_auto_schema(request_body=Applications_serializer)
    @role_required_v2("applications")
    def put(self, request: Request, id: int):
        return update_application(request, id)


class Classificators(APIView):
    def get(self, request: Request):
        return get_all_classificators(request)


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


class Project_type_main(APIView):
    def get(self, request: Request):
        return get_project_type_by_section(request)

    @role_required(allowed_roles=["admin"])
    def post(self, request: Request):
        return create_project_type(request)


class Project_type_detail(APIView):
    @role_required(allowed_roles=["admin"])
    def put(self, request: Request, id: int):
        return update_project_type(request, id)


class Contest_main(APIView):
    def get(self, request: Request):
        return get_contests_by_section(request)

    @role_required(allowed_roles=["admin"])
    def post(self, request: Request):
        return create_contest(request)


class Contest_detail(APIView):
    @role_required(allowed_roles=["admin"])
    def put(self, request: Request, id: int):
        return update_contest(request, id)
