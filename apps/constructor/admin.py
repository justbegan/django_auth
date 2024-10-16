from django.contrib import admin
from django.db import models
from jsoneditor.forms import JSONEditor
from codemirror2.widgets import CodeMirrorEditor
from simple_history.admin import SimpleHistoryAdmin

from .models import (Contest, Status, Application, Project_type, Schema, Document_type, Custom_validation)


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


admin.site.register(Document_type)


@admin.register(Schema)
class Schema_admin(BaseAdmin):
    list_display = ['title', 'section']


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
    history_list_display = ['history_date', 'history_user']


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


admin.site.register(Application.history.model, MyModelHistoryAdmin)
admin.site.register(Contest.history.model, MyModelHistoryAdmin)
