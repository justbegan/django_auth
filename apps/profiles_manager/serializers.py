from rest_framework import serializers

from .models import Profiles_manager_app


class Profiles_manager_app_serializer(serializers.ModelSerializer):
    author_obj = serializers.DictField(read_only=True)
    profile_obj = serializers.DictField(read_only=True)

    class Meta:
        model = Profiles_manager_app
        fields = '__all__'


class Profiles_manager_app_serializer_ff(serializers.Serializer):
    text = serializers.CharField(required=False)
    profile = serializers.IntegerField()
    status = serializers.IntegerField(required=False)
    section = serializers.IntegerField()
