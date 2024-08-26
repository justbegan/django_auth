from rest_framework import serializers

from apps.constructor.models import Application
from apps.constructor.models import Contest, Project_type, Status, Document_type


class Applications_serializer(serializers.ModelSerializer):
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
