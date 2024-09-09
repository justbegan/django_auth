from rest_framework.views import APIView, Response, Request
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from .services.profile_services import (get_profile, get_profile_by_user_id, update_user_data,
                                        update_profile_by_user_id, create_user)
from .serializers import User_serializer


class Profile_main(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(get_profile(request))

    @swagger_auto_schema(request_body=User_serializer)
    def put(self, request):
        return update_user_data(request)

    @swagger_auto_schema(request_body=User_serializer)
    def post(self, request):
        return create_user(request)


class Profile_detail(APIView):
    def get(self, request: Request, id: int):
        return Response(get_profile_by_user_id(id))

    @swagger_auto_schema(request_body=User_serializer)
    def put(self, request: Request, id: int):
        return update_profile_by_user_id(request, id)
