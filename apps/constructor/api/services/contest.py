from rest_framework.views import Request, Response
from .crud import create, update

from ..serializers import Contest_serializer
from ...models import Contest


def create_contest(request: Request):
    return Response(create(Contest_serializer, request.data))


def update_contest(request: Request, id: int):
    return Response(update(Contest, Contest_serializer, request.data, {"id": id}))
