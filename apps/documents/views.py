from rest_framework.views import APIView

from .services import create_document, update_document, get_all_documents


class Document_main(APIView):
    def post(self, request):
        return create_document(request)

    def get(self, request):
        return get_all_documents(request)


class Document_detail(APIView):
    def put(self, request, id):
        return update_document(request, id)
