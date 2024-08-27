from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/municipal_district', views.Municipal_district_main.as_view()),
    path('api/v1/settlement/<int:reg_id>', views.Settlement_detail.as_view()),
    path('api/v1/locality/<int:id>', views.Locality_detail.as_view()),
]
