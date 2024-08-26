from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Request
from rest_framework.permissions import IsAuthenticated

from .serializers import Applications_serializer
from ..models import Application
from .filter import Application_filter
from .services.classificators import get_all_classificators
from .services.applications import get_by_application_id, update_application
from .services.current import get_current_contest, get_current_section


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000


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

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            section=get_current_section(self.request),
            contest=get_current_contest(self.request)
        )


class Application_detail(APIView):
    def get(self, request: Request, id: int):
        return get_by_application_id(request, id)
    
    def put(self, request: Request, id: int):
        return update_application(request, id)


class Classificators(APIView):
    def get(self, request: Request):
        return get_all_classificators()
