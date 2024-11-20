from django.db.models import Model
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
import logging

logger = logging.getLogger('django')


class Base_crud:
    @staticmethod
    def update(model: Model, serializer: ModelSerializer, data: dict, parameters: dict):
        instance = model.objects.get(**parameters)
        serializer = serializer(instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return serializer.data
        raise serializers.ValidationError(serializer.errors)

    @staticmethod
    def get(model: Model, serializer: ModelSerializer, parameters: dict = {}):
        try:
            obj = model.objects.get(**parameters)
            return serializer(obj).data
        except Exception as e:
            logger.exception(f"Ошибка получения данных в crud {e}")
            return {}

    @staticmethod
    def get_many(
        model: Model,
        serializer: ModelSerializer,
        parameters: dict = {},
        order: str = "id",
        custom_obj: dict = None
    ):
        if custom_obj is None:
            obj = model.objects.filter(**parameters).order_by(order)
        else:
            obj = custom_obj
        return serializer(obj, many=True).data

    @staticmethod
    def create(serializer: ModelSerializer, data: dict):
        ser: ModelSerializer = serializer(data=data)
        if ser.is_valid():
            ser.save()
            return ser.data
        else:
            raise serializers.ValidationError(ser.errors)

    @staticmethod
    def delete(model: Model, parameter: dict):
        obj = model.objects.get(**parameter)
        obj.delete()
        return True

    @staticmethod
    def patch(model: Model, serializer: ModelSerializer, data: dict, parameters: dict):
        instance = model.objects.get(**parameters)
        serializer = serializer(instance, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return serializer.data
        raise serializers.ValidationError(serializer.errors)
