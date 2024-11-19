from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import Response
from rest_framework.parsers import MultiPartParser, FormParser
from requests import post
import os
from dotenv import load_dotenv

from services.current import get_current_section
from .serializers import File_handler_serializer

load_dotenv()


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return None


class File_handler_list(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = File_handler_serializer

    def post(self, request):
        data = request.data

        file = request.FILES["file"]
        section = get_current_section(request).tech_name

        file_server_url = os.environ.get('FILE_SERVER')

        files = {"file": (file.name, file.read())}
        data = {"section": section}
        response = post(file_server_url, files=files, data=data)

        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({"error": f"Failed to upload file to server {file_server_url}"}, status=500)
