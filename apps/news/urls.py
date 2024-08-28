from django.urls import path
from . import views


urlpatterns = [
    path("news", views.News_main.as_view()),
    path("news_detail", views.News_detail.as_view())
]
