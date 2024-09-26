from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/users', views.Users_main.as_view()),
    path('api/v1/users/<int:id>', views.Users_detail.as_view()),
    path('api/v1/current_user', views.Current_user.as_view())
]
