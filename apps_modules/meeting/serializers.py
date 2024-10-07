from rest_framework import serializers

from .models import Meeting_schema, Meeting_app, Meeting_document_type, Status


class Meetign_schema_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Meeting_schema


class Meeting_app_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Meeting_app


class Meeting_app_serializer_ff(serializers.Serializer):
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


class Meeting_document_type_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Meeting_document_type


class Meeting_status_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Status
