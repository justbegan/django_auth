from rest_framework.views import APIView, Request, Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .services import News_services
from .serializers import News_serializer_ff, News_serializer
from services.decorators import Decorators
from .models import News
from .filter import News_filter


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


class News_main(generics.ListCreateAPIView):
    model_used = News
    queryset = News.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = News_filter
    serializer_class = News_serializer

    def get_queryset(self):
        q = super().get_queryset()
        return q.order_by('-id')

    @Decorators.role_required_v2()
    @swagger_auto_schema(request_body=News_serializer_ff)
    def post(self, request: Request):
        return News_services.create_news(request)


class News_detail(APIView):
    model_used = News

    def get(self, request: Request, id: int):
        return News_services.get_new_by_id(request, id)

    @Decorators.role_required_v2()
    @swagger_auto_schema(request_body=News_serializer_ff)
    def put(self, request: Request, id: int):
        return News_services.update_news(request, id)

    @Decorators.role_required_v2()
    def delete(self, request: Request, id: int):
        return News_services.delete_news(request, id)
