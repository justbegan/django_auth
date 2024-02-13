from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .services.apigetaway import make_a_request


# class Api_get_away(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request: Request, path: str):
#         return make_a_request(request, path)


@api_view(['POST', 'GET', 'PUT'])
@permission_classes([IsAuthenticated])
def api_getaway(request: Request, path: str):
    return make_a_request(request, path)
