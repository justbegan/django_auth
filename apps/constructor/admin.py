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


admin.site.register(Contest)
admin.site.register(Status)


# @admin.register(Application)
# class Aplication_admin(BaseAdmin):
#     pass


admin.site.register(Project_type)
admin.site.register(Document_type)


@admin.register(Schema)
class Schema_admin(BaseAdmin):
    pass


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
    history_list_display = ['history_date', 'history_user']
