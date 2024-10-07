from rest_framework.views import Response
from rest_framework.serializers import ModelSerializer
from django.db.models import Model

from .current import get_current_section


def get_schema_by_user(request, model: Model, serializer: ModelSerializer):
    obj = model.objects.get(section=get_current_section(request))
    ser = serializer(obj)
    return Response(ser.data)
