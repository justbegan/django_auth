from ..models import Profile
from ..serializers import Profile_serializer
from rest_framework.request import Request
from rest_framework.views import Response
from django.contrib.auth.models import User

from ..serializers import User_serializer
from services.crud import update, get, create


def get_profile(request):
    return get(User, User_serializer, {"id": request.user.id})


def get_profile_by_user_id(user_id: int):
    return get(User, User_serializer, {"id": user_id})


def update_profile_by_user_id(request: Request, user_id: int):
    data = request.data
    profile_id = data['profile']['id']
    profile_data = data['profile']
    user = update(User, User_serializer, data, {"id": user_id})
    profile = update(Profile, Profile_serializer, profile_data, {"user__id": profile_id})
    user['profile'] = profile
    return Response(user)


def update_user_data(request: Request):
    user_id = request.user.id
    data = request.data
    profile_data = data['profile']
    profile_id = data['profile']['id']
    user = update(User, User_serializer, data, {"id": user_id})
    profile = update(Profile, Profile_serializer, profile_data, {"user__id": profile_id})
    user['profile'] = profile
    return Response(user)


def create_user(request: Request):
    data = request.data
    # profile_data = data['profile']
    return Response(create(User_serializer, data))
