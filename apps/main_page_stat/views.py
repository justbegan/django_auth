from rest_framework.views import APIView, Response
from django.db.models import Sum
from django.db.models.expressions import RawSQL
from django.contrib.contenttypes.models import ContentType
import logging

from apps.profiles.models import Section
from apps.locations.models import Municipal_district
from apps.constructor.models import Application, Calculated_fields
from .models import Main_page_stats_mapper


logger = logging.getLogger('django')


class Location_stat(APIView):
    def get(self, request):
        sections = Section.objects.all()
        municipal_districts = Municipal_district.objects.all()
        content_type = ContentType.objects.get_for_model(Main_page_stats_mapper)
        result = []
        for ra in municipal_districts:
            obj = {
                "id": ra.id,
            }
            sections_obj = []
            for section in sections:
                sec = {
                    "id": section.id,
                    "count": Application.objects.filter(section=section, municipal_district=ra).count()
                }
                custom_fields = Calculated_fields.objects.filter(
                    section=section,
                    content_type=content_type,
                    func_type=2
                )
                for calc_field in custom_fields:
                    try:
                        if calc_field.use_sum:
                            sec[calc_field.title] = Application.objects.filter(municipal_district=ra).aggregate(
                                total=Sum(RawSQL(calc_field.code, []))
                            )['total']
                        else:
                            sec[calc_field.title] = Application.objects.filter(municipal_district=ra).aggregate(
                                total=RawSQL(calc_field.code, [])
                            )['total']
                    except Exception as e:
                        logger.exception(f"Ошибка выполнения sql запроса статистики главного окна {e}")
                        sec[calc_field.title] = None

                sections_obj.append(sec)
            obj['sections'] = sections_obj
            result.append(obj)
        return Response(result)

    def test(self, section, content_type):
        Calculated_fields.objects.filter(section=section, content_type=content_type)
