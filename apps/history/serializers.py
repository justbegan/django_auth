from rest_framework import serializers

from .models import History


class History_serializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'
