from rest_framework.views import Request, Response
from django.db.models.expressions import RawSQL
from django.contrib.contenttypes.models import ContentType
import logging
from django.db.models import Sum
from rest_framework.pagination import PageNumberPagination

from apps.constructor.models import Calculated_fields
from .models import Ppmi_report
from services.current import get_current_section

logger = logging.getLogger('django')


class Base_pagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            "fields_description": self.get_fields(),
            'total_results': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

    def get_fields(self):
        return {}


class Ppmi_report_services:
    @classmethod
    def query_handler(cls, request: Request, query: dict) -> dict:
        section = get_current_section(request)
        content_type = ContentType.objects.get_for_model(Ppmi_report)

        calcs_fields = Calculated_fields.objects.filter(
            section=section,
            content_type=content_type,
            func_type=1
        )
        for calc_field in calcs_fields:
            try:
                if calc_field.use_sum:
                    query = query.annotate(**{calc_field.title: Sum(RawSQL(calc_field.code, []))})
                else:
                    query = query.annotate(**{calc_field.title: RawSQL(calc_field.code, [])})
            except Exception as e:
                logger.exception(f"Ошибка выполнения sql запроса в отчете ппми {e}")

        return query.filter(contest__section=section).order_by('-created_at')
