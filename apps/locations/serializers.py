from rest_framework import serializers

from .models import Municipal_district, Settlement, Locality


class Municipal_district_serializer(serializers.ModelSerializer):
    class Meta:
        model = Municipal_district
        fields = '__all__'


class Settlement_serializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = '__all__'


class Locality_serializer(serializers.ModelSerializer):
    class Meta:
        model = Locality
        fields = '__all__'
