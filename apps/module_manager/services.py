from rest_framework.views import Response, Request

from services.crud_services import Base_crud
from .models import Apps
from .serializers import Apps_serializer


def get_all_modules(request: Request):
    return Response(Base_crud.get_many(Apps, Apps_serializer))
