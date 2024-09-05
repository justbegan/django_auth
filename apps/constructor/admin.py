from django.contrib import admin
from django.db import models
from jsoneditor.forms import JSONEditor

from .models import (Contest, Status, Application, Project_type,
                     History, Schema,
                     Main_table_fields)
from .classificators_models import Document_type


class BaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditor(init_options={
            'mode': 'code',
            'indentation': 4,
        }, attrs={'style': 'height: 800px;'})},
    }


admin.site.register(Contest)
admin.site.register(Status)


@admin.register(Application)
class Aplication_admin(BaseAdmin):
    pass


admin.site.register(Project_type)
admin.site.register(History)
admin.site.register(Document_type)


@admin.register(Schema)
class Schema_admin(BaseAdmin):
    pass


admin.site.register(Main_table_fields)
