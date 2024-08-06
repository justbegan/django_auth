from django.db.models import Model
from rest_framework.serializers import ModelSerializer


def update(model: Model, serializer: ModelSerializer, data: dict, parameters: dict):
    instance = model.objects.get(**parameters)
    serializer = serializer(instance, data=data)

    if serializer.is_valid():
        serializer.save()
        return serializer.data
    raise Exception(serializer.errors)


def get(model: Model, serializer: ModelSerializer, parameters: dict):
    obj = model.objects.get(**parameters)
    return serializer(obj).data
