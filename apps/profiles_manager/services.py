from rest_framework.views import Response, Request
from copy import deepcopy
from django.db import transaction

from services.crud_services import Base_crud
from services.current import get_current_section
from .serializers import Profiles_manager_app_serializer
from .models import Profiles_manager_app
from apps.profiles.models import Profile
from users.models import CustomUser
from apps.locations.serializers import Locality_serializer
from apps.profiles.serializers import Profile_serializer


class Profile_manager_services:
    @staticmethod
    def create_locality(data):
        obj = {
            "MunicID": data["settlement"],
            "RegID": data["settlement"],
            "OKTMO": 0,
            "LocName": data["custom_locality"],
            "LocNameE": data["custom_locality"],
            "LocPopulation": 0,
            "LocTypeID": 6
        }
        return Base_crud.create(Locality_serializer, obj)

    @staticmethod
    def create_profile(request, data, new_loc):
        obj = {
            "title": "город Якутск",
            "role": 3,
            "section": get_current_section(request).id,
            "municipal_district": data["municipal_district"],
            "settlement": data["settlement"],
            "locality": new_loc["id"],
            "profile_type": 2,
            "user": data['author'],
            "allowed_number_projects": 1
        }
        return Base_crud.create(Profile_serializer, obj)

    @staticmethod
    def create_profile_manager_app(request: Request):
        data = deepcopy(request.data)
        data['author'] = request.user.id
        return Response(Base_crud.create(Profiles_manager_app_serializer, data))

    @staticmethod
    def update_profile_manager_app(request: Request, id: int):
        data = deepcopy(request.data)
        instance = Profiles_manager_app.objects.get(id=id)
        data['section'] = instance.section.id
        data['author'] = instance.author.id
        return Base_crud.update(Profiles_manager_app, Profiles_manager_app_serializer, data, {"id": id})

    @staticmethod
    def change_profile(profile_id, user_id):
        profile = Profile.objects.get(id=profile_id)
        user = CustomUser.objects.get(id=user_id)
        profile.user = user
        profile.save()

    @staticmethod
    @transaction.atomic
    def update_profile_manager_and_change_profile(request: Request, id: int):
        profile_manger = Profile_manager_services.update_profile_manager_app(request, id)
        if profile_manger['status'] == 2:
            if profile_manger.get('custom_locality'):
                new_loc = Profile_manager_services.create_locality(profile_manger)
                new_profile = Profile_manager_services.create_profile(request, profile_manger, new_loc)
                Profile_manager_services.change_profile(new_profile['id'], profile_manger['author'])
            else:
                Profile_manager_services.change_profile(profile_manger['profile'], profile_manger['author'])
        return Response(profile_manger)
