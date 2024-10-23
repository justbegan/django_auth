from rest_framework import generics, serializers
from .serializers import File_handler_serializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import Response
from rest_framework.parsers import MultiPartParser, FormParser


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return None


class File_handler_list(generics.CreateAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = File_handler_serializer

    def post(self, request):
        data = request.data
        ser = File_handler_serializer(data=data)
        if ser.is_valid():
            ser.save()
            try:
                file = ser.data['file']
                correct_url = "/media/files/" + str(file).split("/media/files/")[1]
                ser.data['file'] = correct_url
            except Exception:
                pass
            return Response(ser.data)
        else:
            raise serializers.ValidationError({"error": "Ошибка при добавлении файла"})
