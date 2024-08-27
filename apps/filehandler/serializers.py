from rest_framework import serializers
from .models import File_handler


class File_handler_serializer(serializers.ModelSerializer):

    class Meta:
        model = File_handler
        fields = ['description', 'file']
