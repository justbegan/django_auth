from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/applications', views.Application_main.as_view()),
    path('api/v1/applications_detial', views.Application_detail.as_view()),
    path('api/v1/classificators', views.Classificators.as_view())
]
