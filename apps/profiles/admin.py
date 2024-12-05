from django.contrib import admin
from .models import (Roles, Profile, Section, Role_handler, Profile_type)
from users.models import CustomUser


admin.site.register(Roles)
admin.site.register(Section)
admin.site.register(Profile_type)


@admin.register(Role_handler)
class Role_handler_admin(admin.ModelAdmin):
    list_display = ['model', 'section']


@admin.register(Profile)
class Profile_admin(admin.ModelAdmin):
    list_display = ['id', 'get_username', 'profile_type',
                    'municipal_district', 'profile_type', 'section', 'locality']
    list_filter = ['section']
    search_fields = ['municipal_district__RegionName', 'municipal_district__RegionNameE']

    def get_username(self, obj):
        try:
            return CustomUser.objects.filter(profile=obj, is_active=True).last().username
        except Exception:
            return "-"
    get_username.short_description = 'Учетная запись'  # Заголовок колонки
