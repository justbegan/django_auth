from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/comment', views.Comment_main.as_view()),
    path('api/v1/comment_detail/<int:id>', views.Comment_detail.as_view()),
]
