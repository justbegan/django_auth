from rest_framework.views import APIView, Request
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .services import get_histories_by_application_id


class History_detail(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'only_status',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description='Filter by active status',
                required=False
            )
        ]
    )
    def get(self, request: Request, id: int):
        only_status = request.query_params.get('only_status', 'true')
        if only_status == 'true':
            only_status = True
        else:
            only_status = False
        return get_histories_by_application_id(request, id, only_status)
