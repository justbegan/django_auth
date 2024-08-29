from rest_framework.views import Request, Response

from ...models import Project_type
from ..serializers import Project_type_serializer
from .crud import get_many
from .current import get_current_section


def get_project_type_by_section(request: Request):
    return Response(get_many(Project_type, Project_type_serializer, {"section": get_current_section(request)}))
