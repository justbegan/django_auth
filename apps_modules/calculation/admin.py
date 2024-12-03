from django.contrib import admin
from django.db import models
from jsoneditor.forms import JSONEditor

from .models import Formula


class Base_formula(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditor(init_options={
            'mode': 'code',
            'indentation': 4,
        }, attrs={'style': 'height: 800px;'})},
    }


@admin.register(Formula)
class Formula_admin(Base_formula):
    list_display = ['title', 'section']
    list_filter = ['section']
