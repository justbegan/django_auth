from rest_framework.views import Response, Request

from services.crud import get_many
from apps.constructor.api.services.current import get_current_section
from .models import Report
from .serializer import Report_serializer


def get_report_by_section(request: Request):
    parameter = {
        "section": get_current_section(request)
    }
    return Response(get_many(Report, Report_serializer, parameter))
