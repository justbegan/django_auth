from rest_framework import serializers

from apps.constructor.models import Application


class Application_registry_serializer(serializers.ModelSerializer):
    municipal_district = serializers.CharField(source='municipal_district.RegionNameE')
    settlement = serializers.CharField(source='settlement.MunicNameE')
    locality = serializers.CharField(source='locality.LocNameE')
    project_type = serializers.CharField(source='project_type.title')
    total_price = serializers.FloatField()

    class Meta:
        model = Application
        fields = ['municipal_district', 'settlement', 'locality', 'title', 'project_type', 'total_price']
