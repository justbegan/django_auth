from rest_framework.views import APIView, Request

from .services import get_histories_by_application_id


class History_detail(APIView):
    def get(self, request: Request, id: int):
        return get_histories_by_application_id(request, id)
