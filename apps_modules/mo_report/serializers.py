from rest_framework import serializers

from .models import Mo_report_schema, Mo_report_app, Mo_report_document_type, Status
from apps.constructor.serializers import Base_applications_serializer, Base_application_serializer_ff


class Meetign_schema_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Mo_report_schema


class Meeting_app_serializer(Base_applications_serializer):
    class Meta:
        fields = '__all__'
        model = Mo_report_app


class Meeting_app_serializer_ff(Base_application_serializer_ff):
    pass


class Meeting_document_type_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Mo_report_document_type


class Meeting_status_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Status
