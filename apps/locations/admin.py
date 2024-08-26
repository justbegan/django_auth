from django.contrib import admin

from .models import Municipal_district, Settlement, Locality, Settlement_type, Locality_type


admin.site.register(Municipal_district)
admin.site.register(Settlement)
admin.site.register(Locality)
admin.site.register(Settlement_type)
admin.site.register(Locality_type)
