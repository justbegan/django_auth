from django.urls import path
from . import views


urlpatterns = [
    path("application_registry", views.Application_registry.as_view())
]
