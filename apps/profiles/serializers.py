from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User


class Profile_serializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # exclude = ['role', 'user']
        fields = '__all__'


class User_serializer(serializers.ModelSerializer):
    profile = Profile_serializer(read_only=True)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'profile', 'username']
