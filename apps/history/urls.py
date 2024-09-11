from django.urls import path
from . import views


urlpatterns = [
    path("history_detail/<int:id>", views.History_detail.as_view()),
    path("history_by_user_id/<int:id>", views.History_by_user_id.as_view()),
    path("history_by_user", views.History_by_user.as_view())
]
