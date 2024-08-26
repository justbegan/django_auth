from django.urls import path
from . import views


urlpatterns = [
    path('create', views.For_test.as_view())
]
