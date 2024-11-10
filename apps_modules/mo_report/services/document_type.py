from apps.constructor.services.document_type import Document_type_base_services

from ..models import Mo_report_document_type
from ..serializers import Mo_report_document_type_serializer


class Document_type_services(Document_type_base_services):
    model = Mo_report_document_type
    serializer = Mo_report_document_type_serializer
