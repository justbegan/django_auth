from rest_framework import serializers
from .models import News


class News_serializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class News_serializer_ff(serializers.Serializer):
    title = serializers.CharField()
    text = serializers.CharField()
