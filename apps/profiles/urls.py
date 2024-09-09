from django.urls import path
from . import views


urlpatterns = [
    path('api', views.Profile_main.as_view()),
    path('api/by_id/<int:id>', views.Profile_detail.as_view())
]
