from django.urls import path
from . import views


urlpatterns = [
    path('ad', views.Ad_main.as_view()),
    path('ad_detail/<int:id>', views.Ad_detail.as_view())
]
