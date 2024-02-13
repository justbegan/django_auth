from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import Response, status
from rest_framework.request import Request


class CustomTokenRefresh(TokenRefreshView):
    def get(self, request: Request):
        cookie_refresh_token = request.COOKIES.get('refresh_token', None)
        if not cookie_refresh_token:
            raise TokenError('No refresh token cookie found')

        refresh_token = {
            "refresh": cookie_refresh_token
        }
        serializer = self.get_serializer(data=refresh_token)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CustomGetToken(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if 'refresh' in response.data:
            response.set_cookie(
                key='refresh_token',
                value=response.data['refresh'],
                httponly=False,
                max_age=30 * 24 * 60 * 60,
                secure=False
            )
        custom_response = {
            "access": response.data["access"]
        }
        return Response(custom_response)
