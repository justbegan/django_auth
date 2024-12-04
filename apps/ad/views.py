from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .services import Ad_services
from .serializers import Ad_serializer_ff


class Ad_main(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'only_active',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                default=1
            )
        ]
    )
    def get(self, request):
        only_active = int(request.GET.get("only_active", '0'))
        if only_active:
            return Ad_services.get_active()
        else:
            return Ad_services.get_all()

    @swagger_auto_schema(request_body=Ad_serializer_ff)
    def post(self, request):
        return Ad_services.create(request)


class Ad_detail(APIView):
    def get(self, request, id):
        return Ad_services.get_by_id(id)

    @swagger_auto_schema(request_body=Ad_serializer_ff)
    def put(self, request, id):
        return Ad_services.update(request, id)

    def delete(self, request, id):
        return Ad_services.delete(id)
