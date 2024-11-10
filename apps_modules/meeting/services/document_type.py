from apps.constructor.services.document_type import Document_type_base_services

from ..models import Meeting_document_type
from ..serializers import Meeting_document_type_serializer


class Document_type_services(Document_type_base_services):
    model = Meeting_document_type
    serializer = Meeting_document_type_serializer
