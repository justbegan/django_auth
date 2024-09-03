from rest_framework import serializers

from apps.constructor.models import Application
from apps.constructor.models import (Contest, Project_type, Status, Document_type, Schema,
                                     Comments, Main_table_fields)


class Applications_serializer(serializers.ModelSerializer):
    point_calculation = serializers.DictField()
    total_point = serializers.FloatField()
    get_financing_republic_grant = serializers.FloatField()
    author_type = serializers.CharField(source='author.profile.profile_type')

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ['author', 'contest', 'section', 'custom_data']


class Contest_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Contest


class Project_type_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Project_type


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


class Comments_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Comments


class Main_table_fields_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Main_table_fields
