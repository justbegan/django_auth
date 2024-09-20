from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/modules', views.Modules.as_view())
]
