from django.contrib import admin
from .models import CustomUser, VerificationCode
from simple_history.admin import SimpleHistoryAdmin
from apps.constructor.admin import MyModelHistoryAdmin


admin.site.register(VerificationCode)


@admin.register(CustomUser)
class CustomUserAdmin(SimpleHistoryAdmin):
    pass


admin.site.register(CustomUser.history.model, MyModelHistoryAdmin)
