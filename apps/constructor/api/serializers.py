from rest_framework import serializers

from apps.constructor.models import Application
from apps.constructor.models import (Contest, Project_type, Status, Schema, Main_table_fields)
from apps.constructor.classificators_models import Document_type


class Applications_serializer(serializers.ModelSerializer):
    point_calculation = serializers.DictField(read_only=True)
    total_point = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    get_financing_republic_grant = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    author_type = serializers.CharField(source='author.profile.profile_type', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ['author', 'contest', 'section']


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


class Main_table_fields_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Main_table_fields
