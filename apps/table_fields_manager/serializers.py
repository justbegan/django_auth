from rest_framework import serializers
from .models import Main_table_fields


class Main_table_fields_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Main_table_fields
