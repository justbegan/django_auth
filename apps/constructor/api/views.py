from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Request

from .serializers import Applications_serializer
from ..models import Application
from .filter import Application_filter
from .services.classificators import get_all_classificators


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000


class Application_main(generics.ListCreateAPIView):
    serializer_class = Applications_serializer
    queryset = Application.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = Application_filter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class Classificators(APIView):
    def get(self, request: Request):
        return get_all_classificators()
