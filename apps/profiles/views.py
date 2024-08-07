from rest_framework.views import APIView, Response
from .services.profile_services import (get_profile, get_profile_by_user_id, update_user_data,
                                        update_profile_by_user_id, create_user)


class Profile_view(APIView):
    def get(self, request):
        return Response(get_profile(request))

    def put(self, request):
        return update_user_data(request)

    def post(self, request):
        return create_user(request)


class Profile_detail(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        return Response(get_profile_by_user_id(user_id))

    def put(self, request):
        user_id = request.GET.get('user_id')
        return update_profile_by_user_id(request, user_id)
