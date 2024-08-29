from rest_framework.views import Request, Response

from ..serializers import Status_serializer
from ...models import Status
from .crud import get_many
from .current import get_current_section


def get_all_statuses_by_section(request: Request):
    return Response(get_many(Status, Status_serializer, {"section": get_current_section(request)}))
