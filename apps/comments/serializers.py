from rest_framework import serializers

from .models import Comments


class Comments_serializer(serializers.ModelSerializer):

    class Meta:
        fields = ['text', 'object_id', 'author', 'content_type']
        model = Comments


class Comments_change_status_serializer(serializers.Serializer):
    text = serializers.CharField()

    def create(self, validated_data):
        return validated_data
