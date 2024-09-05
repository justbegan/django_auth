from rest_framework import serializers

from .models import Comments


class Comments_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Comments
