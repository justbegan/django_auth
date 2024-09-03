from django.contrib import admin

from .models import (Municipal_district, Settlement, Locality, Settlement_type, Locality_type,
                     Region_center)


admin.site.register(Municipal_district)
admin.site.register(Settlement)
admin.site.register(Settlement_type)
admin.site.register(Locality_type)
admin.site.register(Region_center)


@admin.register(Locality)
class Locality_admin(admin.ModelAdmin):
    list_display = ['LocNameE', 'RegID']
    search_fields = ['LocNameE']
