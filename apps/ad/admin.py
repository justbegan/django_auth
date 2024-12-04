from django.contrib import admin

from .models import Ad


@admin.register(Ad)
class Status_admin(admin.ModelAdmin):
    list_display = ['id', 'text', 'author']
