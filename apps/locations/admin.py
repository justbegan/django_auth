from django.contrib import admin

from .models import (Municipal_district, Settlement, Locality, Settlement_type, Locality_type,
                     Region_center, District_type)
from apps.constructor.admin import MyModelHistoryAdmin


@admin.register(Settlement)
class Settlement_admin(admin.Admin):
    list_display = ['id', 'MunicNameE']
    search_fields = ['MunicNameE']


admin.site.register(Settlement_type)
admin.site.register(Locality_type)
admin.site.register(Region_center)
admin.site.register(District_type)


@admin.register(Locality)
class Locality_admin(admin.ModelAdmin):
    list_display = ['LocNameE', 'RegID']
    search_fields = ['LocNameE']


@admin.register(Municipal_district)
class Municipal_district_admin(admin.ModelAdmin):
    list_display = ['id', 'RegionNameE', 'district_type']
    search_fields = ['RegionNameE']


admin.site.register(Locality.history.model, MyModelHistoryAdmin)
