from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import Response
from rest_framework.parsers import MultiPartParser, FormParser
from requests import post

from apps.constructor.services.current import get_current_section
from .serializers import File_handler_serializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return None


class File_handler_list(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = File_handler_serializer

    def post(self, request):
        data = request.data

        file = request.FILES["file"]
        section = str(get_current_section(request).title)

        fastapi_url = "http://10.18.8.15:8080/upload"

        files = {"file": (file.name, file.read())}
        data = {"section": section}
        response = post(fastapi_url, files=files, data=data)

        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({"error": "Failed to upload file to FastAPI"}, status=500)
