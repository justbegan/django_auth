from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/applications', views.Application_main.as_view()),
    path('api/v1/applications_detail/<int:id>', views.Application_detail.as_view()),
    path('api/v1/classificators', views.Classificators.as_view()),
    path('api/v1/schema', views.Schema_main.as_view()),
    path('api/v1/comment', views.Comment_main.as_view()),
    path('api/v1/comment_detail/<int:id>', views.Comment_detail.as_view()),
    path('api/v1/main_table_fields', views.Main_table_fields_main.as_view())
]
