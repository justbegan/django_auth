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


@admin.register(Status)
class Meeting_status_admin(admin.ModelAdmin):
    list_display = ['id', 'title', 'tech_name', 'section']
    list_filter = ['section']


@admin.register(Meeting_document_type)
class Meeting_document_type(admin.ModelAdmin):
    list_display = ['id', 'title', 'section']
    list_filter = ['section']


@admin.register(Meeting_app)
class Meeting_app_admin(BaseAdmin):
    list_display = ['municipal_district', 'locality', 'contest', 'section', 'status']
    list_filter = ['contest', 'section']


@admin.register(Meeting_schema)
class Meeting_schema_admin(BaseAdmin):
    pass
