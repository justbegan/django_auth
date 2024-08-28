from django.urls import path
from . import views


urlpatterns = [
    path("history_detail/<int:id>", views.History_detail.as_view())
]
