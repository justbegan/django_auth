from rest_framework.views import APIView, Request

from .services import create_document, update_document, get_all_documents


class Document_main(APIView):
    def post(self, request: Request):
        return create_document(request)

    def get(self, request: Request):
        return get_all_documents(request)


class Document_detail(APIView):
    def put(self, request: Request, id: int):
        return update_document(request, id)
