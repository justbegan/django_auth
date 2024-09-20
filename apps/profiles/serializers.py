from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Profile, Role_handler, Roles, Section
# from apps.profiles.services.services import get_contest_modules_by_contest_id


class Profile_serializer(serializers.ModelSerializer):
    role_name = serializers.CharField(read_only=True, source='role.title')
    get_modules = serializers.ListField(read_only=True)

    class Meta:
        model = Profile
        # exclude = ['role', 'user']
        fields = '__all__'


class User_serializer(serializers.ModelSerializer):
    profile = Profile_serializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'profile', 'username', 'password']

        extra_kwargs = {
            'password': {'write_only': True}  # Делаем пароль доступным только для записи
        }

    def create(self, validated_data):

        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class Role_handler_serializer(serializers.ModelSerializer):
    class Meta:
        model = Role_handler
        fields = '__all__'
        read_only_fields = ['section']


class Role_serializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'


class Section_serializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'


class Section_serializer_ff(serializers.Serializer):
    title = serializers.CharField()
    logo = serializers.CharField(required=False)
    header = serializers.CharField(required=False)
    modules = serializers.ListField(required=False)
