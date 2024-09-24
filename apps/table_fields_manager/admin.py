from django.contrib import admin
from .models import Main_table_fields


@admin.register(Main_table_fields)
class Call_stat_admin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content_type']
    search_fields = ['title']
    ordering = ()
