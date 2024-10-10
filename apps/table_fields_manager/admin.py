from django.contrib import admin
from .models import Main_table_fields
from django.db import models
from jsoneditor.forms import JSONEditor


class BaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditor(init_options={
            'mode': 'code',
            'indentation': 4,
        }, attrs={'style': 'height: 400px;'})},
    }


@admin.register(Main_table_fields)
class Call_stat_admin(BaseAdmin):
    list_display = ['id', 'title', 'content_type']
    search_fields = ['title']
    ordering = ()
