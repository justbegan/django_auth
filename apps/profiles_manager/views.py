from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import Response, APIView, Request
from rest_framework.permissions import IsAuthenticated

from .serializers import Profiles_manager_app_serializer, Profiles_manager_app_serializer_ff
from .models import Profiles_manager_app
from .filter import Profiles_manager_app_filter
from .services import create_profile_manager_app, update_profile_manager_and_change_profile


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


class Profiles_manager_app_main(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Profiles_manager_app_serializer
    queryset = Profiles_manager_app.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = Profiles_manager_app_filter

    def get_queryset(self):
        return super().get_queryset()

    @swagger_auto_schema(request_body=Profiles_manager_app_serializer_ff)
    def post(self, request, *args, **kwargs):
        return create_profile_manager_app(request)


class Profiles_manager_app_detail(APIView):
    @swagger_auto_schema(request_body=Profiles_manager_app_serializer_ff)
    def put(self, request: Request, id: int):
        return update_profile_manager_and_change_profile(request, id)
