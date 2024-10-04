from django.contrib import admin
from django.db import models
from codemirror2.widgets import CodeMirrorEditor

from .models import Formula


class FormulaAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CodeMirrorEditor(options={
            'mode': 'python',  # Вы можете изменить 'python' на необходимый язык
            'lineNumbers': True,
        }, attrs={'style': 'width: 600px;'})},
    }


admin.site.register(Formula, FormulaAdmin)
