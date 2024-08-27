from rest_framework.views import Response

from .current import get_current_section
from apps.constructor.models import Schema
from ..serializers import Schema_serializer


def get_schema_by_user(request):
    obj = Schema.objects.get(section=get_current_section(request))
    ser = Schema_serializer(obj)
    return Response(ser.data)
