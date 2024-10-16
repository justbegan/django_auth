from rest_framework import serializers

from apps.constructor.models import Application
from apps.constructor.models import (Contest, Project_type, Status, Schema, Document_type)
from apps.comments.serializers import Comments_change_status_serializer


class Base_applications_serializer(serializers.ModelSerializer):
    profile_type = serializers.CharField(source='author.profile_type.title', read_only=True)
    municipal_district_title = serializers.CharField(source='municipal_district.RegionNameE', read_only=True)
    settlement_title = serializers.CharField(read_only=True, source='settlement.MunicNameE')
    locality_title = serializers.CharField(read_only=True, source='locality.LocNameE')
    status_title = serializers.CharField(read_only=True, source='status.title')

    class Meta:
        abstract = True


class Applications_serializer(Base_applications_serializer):
    point_calculation = serializers.DictField(read_only=True)
    total_point = serializers.FloatField(read_only=True)
    get_financing_republic_grant = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    project_type_title = serializers.CharField(read_only=True, source='project_type.title')

    class Meta:
        model = Application
        fields = "__all__"


class Base_application_serializer_ff(serializers.Serializer):
    title = serializers.CharField()
    municipal_district = serializers.IntegerField()
    settlement = serializers.IntegerField()
    locality = serializers.IntegerField()
    status = serializers.IntegerField()
    custom_data = serializers.JSONField()
    documents = serializers.JSONField()

    def update(self, instance, validated_data):
        return validated_data

    def create(self, validated_data):
        return validated_data


class Application_serializer_ff(Base_application_serializer_ff):
    project_type = serializers.IntegerField()
    comment = Comments_change_status_serializer(required=False)


class Application_for_map_serializer(serializers.ModelSerializer):
    get_lat_lon = serializers.JSONField(read_only=True)
    get_project_problem = serializers.CharField(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'title', 'get_project_problem', 'get_lat_lon']


class Contest_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Contest


class Project_type_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Project_type


class Project_type_serializer_ff(serializers.Serializer):
    title = serializers.CharField()


class Status_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Status


class Document_type_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Document_type


class Schema_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Schema


class Application_change_status_serializer(serializers.Serializer):
    contest_id = serializers.IntegerField()
