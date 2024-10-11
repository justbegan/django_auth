from rest_framework import serializers

from .models import Meeting_schema, Meeting_app, Meeting_document_type, Status
from apps.constructor.serializers import Base_applications_serializer, Base_application_serializer_ff


class Meetign_schema_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Meeting_schema


class Meeting_app_serializer(Base_applications_serializer):
    class Meta:
        fields = '__all__'
        model = Meeting_app


class Meeting_app_serializer_ff(Base_application_serializer_ff):
    pass


class Meeting_document_type_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Meeting_document_type


class Meeting_status_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Status
