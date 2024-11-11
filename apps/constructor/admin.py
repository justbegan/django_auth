from django.contrib import admin
from django.db import models
from jsoneditor.forms import JSONEditor
from codemirror2.widgets import CodeMirrorEditor
from simple_history.admin import SimpleHistoryAdmin
import json
from django.utils.safestring import mark_safe
from .models import (Contest, Status, Application, Project_type, Schema, Document_type,
                     Custom_validation, Calculated_fields)


class BaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditor(init_options={
            'mode': 'code',
            'indentation': 4,
        }, attrs={'style': 'height: 800px;'})},
    }


@admin.register(Status)
class Status_admin(admin.ModelAdmin):
    list_display = ['title', 'section']
    list_filter = ['section']


@admin.register(Project_type)
class Project_type_admin(admin.ModelAdmin):
    list_display = ['title', 'section']


@admin.register(Document_type)
class Document_type_admin(admin.ModelAdmin):
    list_display = ['id', 'title', 'section']


@admin.register(Schema)
class Schema_admin(BaseAdmin):
    list_display = ['title', 'section']
    readonly_fields = ('json_field_display',)

    def sort_data_by_pos(self, data):
        # Сортируем элементы словаря, конвертируя 'pos' в float
        sorted_items = sorted(data.items(), key=lambda item: item[1].get("pos", 0))
        # Возвращаем как отсортированный словарь
        return {key: value for key, value in sorted_items}

    def json_field_display(self, obj):
        sorted_data = self.sort_data_by_pos(obj.properties)
        formatted_json = json.dumps(sorted_data, ensure_ascii=False, indent=2)
        # Возвращаем JSON с выделением отступов
        return mark_safe(f'<pre>{formatted_json}</pre>')

    json_field_display.short_description = "Отсортированные данные JSON"


class FormulaAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CodeMirrorEditor(options={
            'mode': 'python',
            'lineNumbers': True,
        }, attrs={'style': 'width: 600px;'})},
    }


admin.site.register(Custom_validation, FormulaAdmin)


@admin.register(Application)
class ApplicationAdmin(SimpleHistoryAdmin, BaseAdmin):
    list_display = ['title', 'contest', 'section', 'status']
    list_filter = ['contest', 'section']
    history_list_display = ['history_date', 'history_user']
    search_fields = ['title']


@admin.register(Contest)
class ContestAdmin(SimpleHistoryAdmin):
    list_display = ['title', 'section', 'status']


class MyModelHistoryAdmin(admin.ModelAdmin):
    list_display = ['history_date', 'history_user', 'history_type', 'get_changes']
    list_filter = ['history_type', 'history_user']
    search_fields = ['id']

    def get_changes(self, obj):
        # Получаем предыдущую запись (если есть)
        prev_record = obj.prev_record

        # Если есть предыдущая запись, сравниваем её с текущей
        if prev_record:
            changes = []
            for field in obj.instance._meta.fields:
                field_name = field.name
                old_value = getattr(prev_record, field_name, None)
                new_value = getattr(obj.instance, field_name, None)
                if old_value != new_value:
                    changes.append(f'{field.verbose_name}: {old_value} ➔➔➔ {new_value}')

            if changes:
                return changes

        return 'Нет изменений'

    get_changes.short_description = 'Изменения'


admin.site.register(Calculated_fields, FormulaAdmin)


admin.site.register(Application.history.model, MyModelHistoryAdmin)
admin.site.register(Contest.history.model, MyModelHistoryAdmin)
