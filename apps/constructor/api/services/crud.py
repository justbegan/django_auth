from django.db.models import Model
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


def update(model: Model, serializer: ModelSerializer, data: dict, parameters: dict):
    instance = model.objects.get(**parameters)
    serializer = serializer(instance, data=data)

    if serializer.is_valid():
        serializer.save()
        return serializer.data
    raise Exception(serializer.errors)


def get(model: Model, serializer: ModelSerializer, parameters: dict = {}):
    obj = model.objects.get(**parameters)
    return serializer(obj).data


def get_many(model: Model, serializer: ModelSerializer, parameters: dict = {}):
    obj = model.objects.filter(**parameters)
    return serializer(obj, many=True).data


def create(serializer: ModelSerializer, data: dict):
    ser: ModelSerializer = serializer(data=data)
    if ser.is_valid():
        ser.save()
        return ser.data
    else:
        raise serializers.ValidationError(ser.errors)


def delete(model: Model, parameter: dict):
    obj = model.objects.get(**parameter)
    obj.delete()
    return True
