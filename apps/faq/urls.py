from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/question', views.Question_main.as_view()),
    path('api/v1/question_detail/<int:id>', views.Question_detail.as_view())
]
