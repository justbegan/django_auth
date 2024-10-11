from .models import Meeting_app
from apps.constructor.filter import Base_application_filter


class Meeting_app_filter(Base_application_filter):
    class Meta:
        models = Meeting_app
        fields = ['id', 'created_at', 'status']
