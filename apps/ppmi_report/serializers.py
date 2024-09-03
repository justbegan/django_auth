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


class Results_of_applications_acceptance_serializer(serializers.ModelSerializer):
    municipal_district = serializers.CharField(source='municipal_district.RegionNameE')
    settlement = serializers.CharField(source='settlement.MunicNameE')
    locality = serializers.CharField(source='locality.LocNameE')
    project_type = serializers.CharField(source='project_type.title')
    total_price = serializers.FloatField()
    get_financing_settlement_budget = serializers.FloatField()
    get_financing_people = serializers.FloatField()
    get_financing_sponsors = serializers.FloatField()
    get_financing_republic_grant = serializers.FloatField()

    class Meta:
        model = Application
        fields = [
            'municipal_district',
            'settlement',
            'locality',
            'title',
            'project_type',
            'total_price',
            'get_financing_settlement_budget',
            'get_financing_people',
            'get_financing_sponsors',
            'get_financing_republic_grant'
        ]


class Application_rating_serializer(serializers.ModelSerializer):
    municipal_district = serializers.CharField(source='municipal_district.RegionNameE')
    settlement = serializers.CharField(source='settlement.MunicNameE')
    locality = serializers.CharField(source='locality.LocNameE')
    get_financing_republic_grant = serializers.FloatField()
    total_point = serializers.FloatField()

    class Meta:
        model = Application
        fields = [
            'municipal_district',
            'settlement',
            'locality',
            'title',
            'get_financing_republic_grant',
            'total_point',
            'created_at'
        ]
