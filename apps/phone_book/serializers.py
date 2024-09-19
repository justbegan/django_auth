from rest_framework import serializers
from .models import Phone_book


class Phone_book_serializer(serializers.ModelSerializer):
    class Meta:
        model = Phone_book
        fields = '__all__'


class Phone_book_serializer_for_swagger(serializers.Serializer):
    fio = serializers.CharField()
    position = serializers.CharField()
    description = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.CharField()