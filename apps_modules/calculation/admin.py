from django.contrib import admin
from django.db import models
from codemirror2.widgets import CodeMirrorEditor

from .models import Formula


class BaseFormula(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CodeMirrorEditor(options={
            'mode': 'python',  # Вы можете изменить 'python' на необходимый язык
            'lineNumbers': True,
        }, attrs={'style': 'width: 600px;'})},
    }


@admin.register(Formula)
class Formula_admin(BaseFormula):
    list_display = ['title', 'section']
    list_filter = ['section']
