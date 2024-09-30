from rest_framework import serializers

from .models import Profiles_manager_app


class Profiles_manager_app_serializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles_manager_app
        fields = '__all__'


class Profiles_manager_app_serializer_ff(serializers.Serializer):
    text = serializers.CharField(required=False)
    profile = serializers.CharField()
    status = serializers.IntegerField(required=False)
