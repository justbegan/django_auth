from rest_framework.views import APIView, Request

from .services import create_document, update_document, get_all_documents
from apps.constructor.services.decorators import role_required


class Document_main(APIView):
    @role_required(allowed_roles=['admin'])
    def post(self, request: Request):
        return create_document(request)

    def get(self, request: Request):
        return get_all_documents(request)


class Document_detail(APIView):
    @role_required(allowed_roles=['admin'])
    def put(self, request: Request, id: int):
        return update_document(request, id)
