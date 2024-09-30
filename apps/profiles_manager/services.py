from rest_framework.views import Response, Request
from copy import deepcopy

from services.crud import create, update
from apps.constructor.services.current import get_current_section
from .serializers import Profiles_manager_app_serializer
from .models import Profiles_manager_app


def create_profile_manager_app(request: Request):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request).id
    data['author'] = request.user.id
    return Response(create(Profiles_manager_app_serializer, data))


def update_profile_manager_app(request: Request, id: int):
    data = deepcopy(request.data)
    instance = Profiles_manager_app.objects.get(id=id)
    data['section'] = instance.section.id
    data['author'] = instance.author.id
    return Response(update(Profiles_manager_app, Profiles_manager_app_serializer, data, {"id": id}))
