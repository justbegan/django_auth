from rest_framework.views import Request, Response
from django.utils.timezone import now

from services.crud_services import Base_crud
from .models import Ad
from .serializers import Ad_serializer


class Ad_services:
    model = Ad
    serializer = Ad_serializer

    @classmethod
    def get_all(cls):
        return Response(Base_crud.get_many(cls.model, cls.serializer))

    @classmethod
    def get_active(cls):
        parameters = {
            "start_date__lte": now(),
            "end_date__gte": now()
        }
        obj = Base_crud.get_many(cls.model, cls.serializer, parameters)
        return Response(obj)

    @classmethod
    def get_by_id(cls, id: int):
        return Response(Base_crud.get(cls.model, cls.serializer, {"id": id}))

    @classmethod
    def create(cls, request: Request):
        data = request.data
        data['author'] = request.user.id
        return Response(Base_crud.create(cls.serializer, data))

    @classmethod
    def update(cls, request: Request, id: int):
        data = request.data
        return Response(Base_crud.patch(cls.model, cls.serializer, data, {"id": id}))

    @classmethod
    def delete(cls, id: int):
        return Response(Base_crud.delete(cls.model, {"id": id}))
