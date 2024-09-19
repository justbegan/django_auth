from django.urls import path
from . import views


urlpatterns = [
    path("letter", views.Letter_main.as_view()),
    path("letter_detailk/<int:id>", views.Letter_detail.as_view())
]
