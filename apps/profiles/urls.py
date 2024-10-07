from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/role', views.Role_main.as_view()),
    path('api/v1/role/<int:id>', views.Role_detail.as_view()),
    path('api/v1/role_handler', views.Role_handler_main.as_view()),
    path('api/v1/role_handler_detail/<int:id>', views.Role_handler_detail.as_view()),
    path('api/v1/role_handler_models', views.Model_main.as_view()),
    path('api/v1/section', views.Section_main.as_view()),
    path('api/v1/section_detail/<int:id>', views.Section_detail.as_view()),
    path('api/v1/profile_type', views.Profile_type_main.as_view()),
]
