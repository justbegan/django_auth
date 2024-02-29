from rest_framework.views import APIView, Response
from .services.get_profile import get_profile


class Profile_view(APIView):
    def get(self, request):
        return Response(get_profile(request))
