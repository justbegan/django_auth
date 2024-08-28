from django.contrib import admin

from .models import (Contest, Status, Application, Project_type,
                     History, Comments, Document, Document_type, Schema,
                     Main_table_fields)


admin.site.register(Contest)
admin.site.register(Status)
admin.site.register(Application)
admin.site.register(Project_type)
admin.site.register(History)
admin.site.register(Comments)
admin.site.register(Document)
admin.site.register(Document_type)
admin.site.register(Schema)
admin.site.register(Main_table_fields)
