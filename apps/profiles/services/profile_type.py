from rest_framework.views import Response, Request

from apps.profiles.models import Profile_type
from apps.profiles.serializers import Profile_type_serializer


def get_all_profile_types(request: Request):
    obj = Profile_type.objects.all()
    ser = Profile_type_serializer(obj, many=True)
    return Response(ser.data)
