from rest_framework.views import Response

from apps.constructor.models import Contest, Project_type, Status, Document_type
from apps.constructor.api.serializers import (Contest_serializer, Project_type_serializer,
                                              Status_serializer, Document_type_serializer)


def get_all_classificators() -> Response:
    result = [
        {
            "title": "Конкурсы",
            "data": Contest_serializer(Contest.objects.all(), many=True).data,
        },
        {
            "title": "Типология проекта",
            "data": Project_type_serializer(Project_type.objects.all(), many=True).data
        },
        {
            "title": "Статусы",
            "data": Status_serializer(Status.objects.all(), many=True).data
        },
        {
            "title": "Типы документов",
            "data": Document_type_serializer(Document_type.objects.all(), many=True).data
        }
    ]
    return Response(result)
