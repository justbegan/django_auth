from django.contrib import admin
from .models import (Roles, Profile, Section, Role_handler)

admin.site.register(Roles)
admin.site.register(Profile)
admin.site.register(Section)
admin.site.register(Role_handler)
