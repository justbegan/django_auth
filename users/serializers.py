from rest_framework import serializers
from users.models import CustomUser

from apps.profiles.serializers import Profile_serializer


class User_serializer(serializers.ModelSerializer):
    profile_obj = Profile_serializer(source='profile', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'is_active', 'profile_obj', 'profile', 'email',
                  'first_name', 'middle_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class User_serializer_ff(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    municipal_district_id = serializers.IntegerField(required=True)
    settlement_id = serializers.IntegerField()
    locality_id = serializers.IntegerField()

    def create(self, validated_data):
        return validated_data
