from django.contrib import admin
from django.db import models
from jsoneditor.forms import JSONEditor

from .models import Mo_report_app, Status, Mo_report_schema, Mo_report_document_type


class BaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditor(init_options={
            'mode': 'code',
            'indentation': 4,
        }, attrs={'style': 'height: 800px;'})},
    }


admin.site.register(Status)
admin.site.register(Mo_report_document_type)


@admin.register(Mo_report_app)
class Meeting_app_admin(BaseAdmin):
    pass


@admin.register(Mo_report_schema)
class Meeting_schema_admin(BaseAdmin):
    pass
