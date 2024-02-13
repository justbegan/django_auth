from rest_framework_simplejwt.views import TokenViewBase, TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import Response, status


class CustomTokenRefresh(TokenViewBase):
    def post(self, request):
        try:
            # Извлечение refresh токена из куки
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                raise TokenError('No refresh token cookie found')

            # Обновление токена
            refresh_token = RefreshToken(refresh_token)
            access_token = refresh_token.access_token

        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'access_token': str(access_token)})


class CustomGetToken(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if 'refresh' in response.data:
            response.set_cookie(
                key='refresh_token',
                value=response.data['refresh'],
                httponly=True,
                max_age=30 * 24 * 60 * 60,
                secure=True
            )
        return response
