from rest_framework.views import Response, Request
from copy import deepcopy
from django.db import transaction

from services.crud import create, update
from .serializers import Profiles_manager_app_serializer
from .models import Profiles_manager_app
from apps.profiles.models import Profile
from users.models import CustomUser


def create_profile_manager_app(request: Request):
    data = deepcopy(request.data)
    data['author'] = request.user.id
    return Response(create(Profiles_manager_app_serializer, data))


def update_profile_manager_app(request: Request, id: int):
    data = deepcopy(request.data)
    instance = Profiles_manager_app.objects.get(id=id)
    data['section'] = instance.section.id
    data['author'] = instance.author.id
    return update(Profiles_manager_app, Profiles_manager_app_serializer, data, {"id": id})


def change_profile(profile_id, user_id):
    profile = Profile.objects.get(id=profile_id)
    user = CustomUser.objects.get(id=user_id)
    profile.user = user
    profile.save()


@transaction.atomic
def update_profile_manager_and_change_profile(request: Request, id: int):
    profile_manger = update_profile_manager_app(request, id)
    if profile_manger['status'] == '2':
        change_profile(profile_manger['profile'], profile_manger['author'])
    return Response(profile_manger)
