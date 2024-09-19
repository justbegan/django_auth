from rest_framework import serializers

from .models import Meeting_schema, Meeting_app


class Meetign_schema_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Meeting_schema


class Meeting_app_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Meeting_app
        read_only_fields = ['author', 'contest', 'section']
