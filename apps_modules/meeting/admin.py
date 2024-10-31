from django.contrib import admin
from django.db import models
from jsoneditor.forms import JSONEditor

from .models import Meeting_app, Status, Meeting_schema, Meeting_document_type


class BaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditor(init_options={
            'mode': 'code',
            'indentation': 4,
        }, attrs={'style': 'height: 800px;'})},
    }


admin.site.register(Status)
admin.site.register(Meeting_document_type)


@admin.register(Meeting_app)
class Meeting_app_admin(BaseAdmin):
    list_display = ['municipal_district', 'locality', 'contest', 'section', 'status']
    list_filter = ['contest', 'section']


@admin.register(Meeting_schema)
class Meeting_schema_admin(BaseAdmin):
    pass
