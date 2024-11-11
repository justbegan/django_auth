from rest_framework import serializers

from apps.constructor.models import Application, Calculated_fields
from apps.constructor.models import (Contest, Project_type, Status, Schema, Document_type)
from apps.comments.serializers import Comments_change_status_serializer


class Base_applications_serializer(serializers.ModelSerializer):
    profile_type = serializers.CharField(source='author.profile_type.title', read_only=True)
    municipal_district_title = serializers.CharField(source='municipal_district.RegionNameE', read_only=True)
    settlement_title = serializers.CharField(read_only=True, source='settlement.MunicNameE')
    locality_title = serializers.CharField(read_only=True, source='locality.LocNameE')
    status_title = serializers.CharField(read_only=True, source='status.title')

    class Meta:
        abstract = True


# class Applications_serializer(Base_applications_serializer):
#     point_calculation = serializers.DictField(read_only=True)
#     total_point = serializers.FloatField(read_only=True)
#     # get_financing_republic_grant = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)
#     # total_price = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)
#     project_type_title = serializers.CharField(read_only=True, source='project_type.title')

#     class Meta:
#         model = Application
#         fields = "__all__"


class Applications_serializer(Base_applications_serializer):
    point_calculation = serializers.DictField(read_only=True)
    total_point = serializers.FloatField(read_only=True)
    project_type_title = serializers.CharField(read_only=True, source='project_type.title')

    class Meta:
        model = Application
        fields = '__all__'

    @staticmethod
    def create_dynamic_method(value):
        # Возвращает динамический метод, который использует значение из параметра
        def dynamic_method(self, obj):
            return eval(value)
        return dynamic_method

    def get_fields(self):
        # Получаем базовые поля, определённые в Meta
        fields = super().get_fields()

        # Динамически добавляем поля из Calculated_fields
        calcs_fields = Calculated_fields.objects.all()

        for param in calcs_fields:
            # Добавляем поле, если его нет в fields
            if param.title not in fields:
                fields[param.title] = serializers.SerializerMethodField()

                # Создаём уникальный метод для каждого динамического поля
                method_name = f'get_{param.title}'
                
                # Проверка, чтобы метод не добавлялся повторно
                if not hasattr(self.__class__, method_name):
                    # Добавляем метод на уровне класса
                    setattr(self.__class__, method_name, self.create_dynamic_method(param.code))

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
