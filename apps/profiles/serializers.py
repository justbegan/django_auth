from rest_framework import serializers

from .models import Profile, Role_handler, Roles, Section, Profile_type


class Profile_serializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    role_name = serializers.CharField(read_only=True, source='role.title')
    get_modules = serializers.ListField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


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
    modules_data = serializers.ListField(read_only=True)

    class Meta:
        model = Section
        exclude = ['modules']


class Section_serializer_ff(serializers.Serializer):
    title = serializers.CharField()
    logo = serializers.CharField(required=False)
    header = serializers.CharField(required=False)
    modules = serializers.ListField(required=False)


class Profile_type_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Profile_type
