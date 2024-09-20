from rest_framework.views import Response, Request

from services.crud import get_many
from .models import Apps
from .serializers import Apps_serializer


def get_all_modules(request: Request):
    return Response(get_many(Apps, Apps_serializer))
