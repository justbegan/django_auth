from rest_framework.views import APIView, Request

from .services import create_document, update_document, get_all_documents
from services.decorators import Decorators
from .models import Document


class Document_main(APIView):
    model_used = Document

    @Decorators.role_required_v2()
    def post(self, request: Request):
        return create_document(request)

    def get(self, request: Request):
        return get_all_documents(request)


class Document_detail(APIView):
    model_used = Document

    @Decorators.role_required_v2()
    def put(self, request: Request, id: int):
        return update_document(request, id)
