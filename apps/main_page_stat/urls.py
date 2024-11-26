from django.urls import path
from . import views


urlpatterns = [
    path('', views.Location_stat.as_view())
]
