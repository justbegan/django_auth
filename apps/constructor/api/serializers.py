from rest_framework import serializers

from apps.constructor.models import Application
from apps.constructor.models import (Contest, Project_type, Status, Schema, Main_table_fields, Document_type)
from apps.comments.serializers import Comments_change_status_serializer


class Applications_serializer(serializers.ModelSerializer):
    point_calculation = serializers.DictField(read_only=True)
    total_point = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    get_financing_republic_grant = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    author_type = serializers.CharField(source='author.profile.profile_type', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Application
        fields = "__all__"


class Application_serializer_ff(serializers.Serializer):
    """
    Кастомный сериализатор для изменения заявки
    из-за создания комментария и изменения статуса
    """
    title = serializers.CharField()
    municipal_district = serializers.IntegerField()
    settlement = serializers.IntegerField()
    locality = serializers.IntegerField()
    project_type = serializers.IntegerField()
    status = serializers.IntegerField()
    custom_data = serializers.JSONField()
    documents = serializers.JSONField()
    comment = Comments_change_status_serializer(required=False)

    def update(self, instance, validated_data):
        return validated_data

    def create(self, validated_data):
        return validated_data


class Application_for_map_serializer(serializers.ModelSerializer):
    get_lat_lon = serializers.JSONField(read_only=True)
    get_project_prolbem = serializers.CharField(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'title', 'get_project_prolbem', 'get_lat_lon']


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


class Main_table_fields_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Main_table_fields
