from rest_framework import serializers

from apps.constructor.models import Application


class Application_registry_serializer(serializers.ModelSerializer):
    municipal_district = serializers.CharField(source='municipal_district.RegionNameE')
    settlement = serializers.CharField(source='settlement.MunicNameE')
    locality = serializers.CharField(source='locality.LocNameE')
    project_type = serializers.CharField(source='project_type.title')
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = Application
        fields = ['municipal_district', 'settlement', 'locality', 'title', 'project_type', 'total_price']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total_price'] = self.format_number(data['total_price'])
        return data

    def format_number(self, value):
        try:
            number = float(value)
            return f"{number:,.2f}".replace(",", " ")
        except (ValueError, TypeError):
            return value


class Results_of_applications_acceptance_serializer(serializers.ModelSerializer):
    municipal_district = serializers.CharField(source='municipal_district.RegionNameE')
    settlement = serializers.CharField(source='settlement.MunicNameE')
    locality = serializers.CharField(source='locality.LocNameE')
    project_type = serializers.CharField(source='project_type.title')
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    get_financing_settlement_budget = serializers.DecimalField(max_digits=12, decimal_places=2)
    get_financing_people = serializers.DecimalField(max_digits=12, decimal_places=2)
    get_financing_sponsors = serializers.DecimalField(max_digits=12, decimal_places=2)
    get_financing_republic_grant = serializers.DecimalField(max_digits=12, decimal_places=2)

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total_price'] = self.format_number(data['total_price'])
        data['get_financing_settlement_budget'] = self.format_number(data['get_financing_settlement_budget'])
        data['get_financing_people'] = self.format_number(data['get_financing_people'])
        data['get_financing_sponsors'] = self.format_number(data['get_financing_sponsors'])
        data['get_financing_republic_grant'] = self.format_number(data['get_financing_republic_grant'])
        return data

    def format_number(self, value):
        try:
            number = float(value)
            return f"{number:,.2f}".replace(",", " ")
        except (ValueError, TypeError):
            return value


class Application_rating_serializer(serializers.ModelSerializer):
    municipal_district = serializers.CharField(source='municipal_district.RegionNameE')
    settlement = serializers.CharField(source='settlement.MunicNameE')
    locality = serializers.CharField(source='locality.LocNameE')
    get_financing_republic_grant = serializers.DecimalField(max_digits=12, decimal_places=2)
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['get_financing_republic_grant'] = self.format_number(
            data['get_financing_republic_grant'])
        return data

    def format_number(self, value):
        try:
            number = float(value)
            return f"{number:,.2f}".replace(",", " ")
        except (ValueError, TypeError):
            return value


class Application_stat_by_district_serializer(serializers.Serializer):
    municipal_district = serializers.CharField()
    settlement_count = serializers.CharField()
    application_count = serializers.CharField()
    settlement_app_percent = serializers.CharField()
    application_winner_count = serializers.CharField()
    application_winner_percent = serializers.CharField()
    application_financing_settlement_budget = serializers.DecimalField(max_digits=12, decimal_places=2)
    application_financing_people = serializers.DecimalField(max_digits=12, decimal_places=2)
    application_financing_sponsors = serializers.DecimalField(max_digits=12, decimal_places=2)
    application_financing_republic_grant = serializers.DecimalField(max_digits=12, decimal_places=2)
    application_finded_sum_percent = serializers.CharField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['settlement_app_percent'] = self.format_percent(data['settlement_app_percent'])
        data['application_winner_percent'] = self.format_percent(data['application_winner_percent'])
        data['application_finded_sum_percent'] = self.format_percent(data['application_finded_sum_percent'])

        data['application_financing_settlement_budget'] = self.format_number(
            data['application_financing_settlement_budget'])
        data['application_financing_people'] = self.format_number(
            data['application_financing_people'])
        data['application_financing_sponsors'] = self.format_number(
            data['application_financing_sponsors'])
        data['application_financing_republic_grant'] = self.format_number(
            data['application_financing_republic_grant'])
        return data

    def format_percent(self, value):
        try:
            percent_value = float(value)
            return f"{percent_value:.2f}%"
        except (ValueError, TypeError):
            return value

    def format_number(self, value):
        try:
            number = float(value)
            return f"{number:,.2f}".replace(",", " ")
        except (ValueError, TypeError):
            return value
