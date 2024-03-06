from django.urls import path
from . import views


urlpatterns = [
    path('api', views.Profile_view.as_view()),
    path('api/by_id', views.Profile_by_user_id.as_view())
]
