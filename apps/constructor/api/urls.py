from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/applications', views.Application_main.as_view(), name='application_main'),
    path('api/v1/applications_detail/<int:id>', views.Application_detail.as_view(), name='application_detail'),
    path('api/v1/applications_for_map', views.Application_for_map.as_view(), name='application_for_map_main'),
    path('api/v1/schema', views.Schema_main.as_view()),
    path('api/v1/main_table_fields', views.Main_table_fields_main.as_view()),
    path('api/v1/status', views.Status_main.as_view()),
    path('api/v1/status_detail/<int:id>', views.Status_detail.as_view()),
    path('api/v1/project_type', views.Project_type_main.as_view()),
    path('api/v1/project_type_detail/<int:id>', views.Project_type_detail.as_view()),
    path('api/v1/contest', views.Contest_main.as_view()),
    path('api/v1/contest_detail/<int:id>', views.Contest_detail.as_view()),
    path('api/v1/document_type', views.Document_type_main.as_view()),
    path('api/v1/document_type_detail/<int:id>', views.Document_type_detail.as_view())
]
