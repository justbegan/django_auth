from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
from apps.profiles.services.services import get_contest_modules_by_contest_id


class Profile_serializer(serializers.ModelSerializer):
    role_name = serializers.CharField(read_only=True, source='role.title')

    class Meta:
        model = Profile
        # exclude = ['role', 'user']
        fields = '__all__'


class User_serializer(serializers.ModelSerializer):
    profile = Profile_serializer(read_only=True)
    modules = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'profile', 'username', 'modules', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_modules(self, obj):
        try:
            contest_id = Profile.objects.get(user=obj).contest
        except:
            raise Exception("user profile not found")
        return get_contest_modules_by_contest_id(contest_id)
