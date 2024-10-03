from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/users', views.Users_main.as_view(), name='users_main'),
    path('api/v1/users/<int:id>', views.Users_detail.as_view()),
    path('api/v1/current_user', views.Current_user.as_view(), name='current_user'),
    path('verify-code/', views.Verify_code.as_view(), name='verify-code'),
    path('repeat-code/', views.Repeat_email.as_view(), name='repeat-code'),
    path('recover-password/', views.Recover_password.as_view())
]
