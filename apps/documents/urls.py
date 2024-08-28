from django.urls import path
from . import views


urlpatterns = [
    path("documents", views.Document_main.as_view()),
    path("documents_detail/<int:id>", views.Document_detail.as_view())
]
