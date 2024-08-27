from rest_framework import serializers
from .models import Document


class Document_serializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
