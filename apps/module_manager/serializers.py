from rest_framework import serializers

from .models import Apps


class Apps_serializer(serializers.ModelSerializer):
    class Meta:
        model = Apps
        fields = '__all__'
