from django.contrib import admin

from .models import News


@admin.register(News)
class News_admin(admin.ModelAdmin):
    list_display = ['id', 'title', 'section']
    list_filter = ['section']
