from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAuthenticated

from .serializers import Applications_serializer
from ..models import Application
from .filter import Application_filter
from .services.classificators import get_all_classificators
from .services.applications import get_by_application_id, update_application
from .services.current import get_current_contest, get_current_section, get_current_new_status
from .services.schema import get_schema_by_user
from .services.custom_data import validate_custom_data
from .services.comment import get_comments_by_application_id, create_comments


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

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['status'] = get_current_new_status(request)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            custom_data=validate_custom_data(request),
            author=self.request.user,
            section=get_current_section(request),
            contest=get_current_contest(request)
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Application_detail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, id: int):
        return get_by_application_id(request, id)

    def put(self, request: Request, id: int):
        return update_application(request, id)


class Classificators(APIView):
    def get(self, request: Request):
        return get_all_classificators()


class Schema_main(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        return get_schema_by_user(request)


class Comment_main(APIView):

    def post(self, request: Request):
        return create_comments(request)


class Comment_detail(APIView):
    """
    Получить все комменты по id заявки
    """
    def get(self, request: Request, id: int):
        return get_comments_by_application_id(request, id)