from django.urls import path
from . import views


urlpatterns = [
    path("application_registry", views.Application_registry.as_view()),
    path("results_of_applications_acceptance", views.Results_of_applications_acceptance.as_view())
]
