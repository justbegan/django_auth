from django.urls import path
from . import views


urlpatterns = [
    path("phone_book", views.Phone_book_main.as_view()),
    path("phone_book/<int:id>", views.Phone_book_details.as_view())
]
