from rest_framework.views import APIView, Request

from .services import get_report_by_section


class Report_main(APIView):
    def get(self, request: Request):
        return get_report_by_section(request)
