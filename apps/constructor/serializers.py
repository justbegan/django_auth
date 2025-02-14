from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from apps.constructor.models import Application, Calculated_fields
from apps.constructor.models import (Contest, Project_type, Status, Schema, Document_type)
from apps.comments.serializers import Comments_change_status_serializer
from services.current import get_current_section


class Base_applications_serializer(serializers.ModelSerializer):
    profile_type = serializers.CharField(source='author.profile_type.title', read_only=True)
    municipal_district_title = serializers.CharField(source='municipal_district.RegionNameE', read_only=True)
    settlement_title = serializers.CharField(read_only=True, source='settlement.MunicNameE')
    locality_title = serializers.CharField(read_only=True, source='locality.LocNameE')
    status_title = serializers.CharField(read_only=True, source='status.title')

    class Meta:
        abstract = True


class Applications_serializer(Base_applications_serializer):
    point_calculation = serializers.DictField(read_only=True)
    total_point = serializers.FloatField(read_only=True)
    project_type_title = serializers.CharField(read_only=True, source='project_type.title')
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Application
        fields = '__all__'

    def get_fields(self):
        # Получаем базовые поля, определённые в Meta
        fields = super().get_fields()
        request = self.context.get('request', None)
        if request.user.is_authenticated:
            section = get_current_section(request)
            content_type = ContentType.objects.get_for_model(Application)
            # Динамически добавляем поля из Calculated_fields
            calcs_fields = Calculated_fields.objects.filter(
                section=section,
                content_type=content_type,
                func_type=1,
                use_sum=False
            )

            for param in calcs_fields:
                # Добавляем поле, если его нет в fields
                if param.title not in fields:
                    """
                        (1, "IntegerField"),
                        (2, "CharField"),
                        (3, "FloatField"),
                        (4, "DecimalField"),
                    """
                    mapping = {
                        1: serializers.IntegerField(read_only=True),
                        2: serializers.CharField(read_only=True),
                        3: serializers.FloatField(read_only=True),
                        4: serializers.DecimalField(read_only=True, max_digits=20, decimal_places=2)
                    }
                    fields[param.title] = mapping[param.field_type]

            # Удаляем динамические поля, которых больше нет в Calculated_fields
            calculated_titles = {param.title for param in calcs_fields}
            fields_to_remove = [name for name in fields if name not in calculated_titles and name.startswith('get_')]
            for name in fields_to_remove:
                fields.pop(name, None)

        return fields


class Base_application_serializer_ff(serializers.Serializer):
    title = serializers.CharField()
    municipal_district = serializers.IntegerField()
    settlement = serializers.IntegerField()
    locality = serializers.IntegerField()
    status = serializers.IntegerField()
    custom_data = serializers.JSONField()
    documents = serializers.JSONField()

    def update(self, instance, validated_data):
        return validated_data

    def create(self, validated_data):
        return validated_data


class Application_serializer_ff(Base_application_serializer_ff):
    project_type = serializers.IntegerField()
    comment = Comments_change_status_serializer(required=False)


class Application_for_map_serializer(serializers.ModelSerializer):
    get_lat_lon = serializers.JSONField(read_only=True)
    get_project_problem = serializers.CharField(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'title', 'get_project_problem', 'get_lat_lon']


class Contest_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Contest


class Project_type_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Project_type


class Project_type_serializer_ff(serializers.Serializer):
    title = serializers.CharField()


class Status_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Status


class Document_type_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Document_type


class Schema_serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Schema


class Application_change_status_serializer(serializers.Serializer):
    contest_id = serializers.IntegerField()
