from django.urls import path
from . import views


urlpatterns = [
    path("", views.File_handler_list.as_view())
]
