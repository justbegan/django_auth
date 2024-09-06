from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/applications', views.Meeting_application_main.as_view()),
    path('api/v1/applications_detail/<int:id>', views.Meeting_application_detail.as_view())
]
