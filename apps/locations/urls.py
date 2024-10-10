from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/municipal_district', views.Municipal_district_main.as_view()),
    path('api/v1/municipal_district_detail/<int:id>', views.Municipal_district_detail.as_view()),

    path('api/v1/settlement_detail/<int:id>', views.Settlement_detail.as_view()),
    path('api/v1/settlement', views.Settlement_main.as_view()),

    path('api/v1/locality_detail/<int:id>', views.Locality_detail.as_view()),
    path('api/v1/locality', views.Locality_main.as_view()),

    path('test', views.CreateLocality.as_view())
]
