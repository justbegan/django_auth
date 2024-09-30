from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/application', views.Profiles_manager_app_main.as_view()),
    path('api/v1/application_detail/<int:id>', views.Profiles_manager_app_detail.as_view())
]
