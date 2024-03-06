from ..models import Profile
from ..serializers import Profile_serializer
from rest_framework.request import Request
from rest_framework.views import Response
from django.contrib.auth.models import User

from ..serializers import User_serializer


def get_profile(request):
    obj = User.objects.get(id=request.user.id)
    ser = User_serializer(obj)
    return ser.data


def get_profile_by_user_id(user_id: int):
    obj = User.objects.get(id=user_id)
    ser = User_serializer(obj)
    return ser.data


def update_user_data(request: Request):
    user_id = request.user.id
    data = request.data
    profile_data = data['profile']
    profile_id = data['profile']['id']
    user = update_user(user_id, data)
    profile = update_profile(profile_id, profile_data)
    user['profile'] = profile
    return Response(user)


def update_user(user_id, data):
    instance = User.objects.get(id=user_id)
    serializer = User_serializer(instance, data=data)

    if serializer.is_valid():
        serializer.save()
        return serializer.data
    raise Exception(serializer.errors)


def update_profile(profile_id, data):
    instance = Profile.objects.get(user__id=profile_id)
    serializer = Profile_serializer(instance, data=data)

    if serializer.is_valid():
        serializer.save()
        return serializer.data
    raise Exception(serializer.errors)
