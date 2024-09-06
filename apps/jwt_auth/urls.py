# from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from django.urls import path
from . import views


urlpatterns = [
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('api/register', include('djoser.urls')),
    # custom
    path('api/token/customRefresh', views.CustomTokenRefresh.as_view()),
    path('api/token/customGetToken', views.CustomGetToken.as_view())
]
