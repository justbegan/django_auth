from django.contrib import admin
from django.db import models
from jsoneditor.forms import JSONEditor
import json
from django.utils.safestring import mark_safe

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
    list_display = ['municipal_district', 'section']
    list_filter = ['contest', 'section']


@admin.register(Mo_report_schema)
class Meeting_schema_admin(BaseAdmin):
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
