from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/applications', views.Application_main.as_view()),
    path('api/v1/applications_detail/<int:id>', views.Application_detail.as_view()),
    path('api/v1/schema', views.Schema_main.as_view()),
    path('api/v1/document_type', views.Document_type_main.as_view()),
    path('api/v1/status', views.Status_main.as_view())
]
