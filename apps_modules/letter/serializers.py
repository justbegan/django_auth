from rest_framework import serializers

from .models import Letter


class Letter_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Letter


class Letter_serializer_ff(serializers.Serializer):
    text = serializers.CharField()
