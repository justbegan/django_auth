
from rest_framework import serializers
from .models import Ad


class Ad_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ad


class Ad_serializer_ff(serializers.Serializer):
    text = serializers.CharField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    def update(self, instance, validated_data):
        return validated_data

    def create(self, validated_data):
        return validated_data
