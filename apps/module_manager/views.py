from rest_framework.views import APIView, Request

from .services import get_all_modules


class Modules(APIView):
    def get(self, request: Request):
        return get_all_modules(request)
