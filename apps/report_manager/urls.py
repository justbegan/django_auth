from django.urls import path
from . import views


urlpatterns = [
    path("report", views.Report_main.as_view())
]
