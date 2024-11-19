from rest_framework.views import Response
from rest_framework.serializers import ModelSerializer
from django.db.models import Model

from services.current import get_current_contest


def get_schema_by_user(request, model: Model, serializer: ModelSerializer):
    obj = model.objects.get(contests=get_current_contest(request))
    ser = serializer(obj)
    return Response(ser.data)
