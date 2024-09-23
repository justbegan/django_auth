from rest_framework.views import Request, Response
from decimal import Decimal
from copy import deepcopy
from django.db import transaction

from apps.constructor.models import Application, Contest
from services.crud import update, get
from .custom_data import validate_custom_data
from .current import get_current_section
from .document import document_validation
from apps.comments.services import create_comment_and_change_status


class Application_service:
    serializer_class = None

    @transaction.atomic
    def update_application(self, request: Request, id: int) -> Response:
        data = deepcopy(request.data)
        validate_custom_data(request)
        document_validation(request)
        instance = Application.objects.get(id=id)
        data['author'] = instance.author.id
        data['section'] = instance.section.id
        data['contest'] = instance.contest.id
        obj = update(Application, self.serializer_class, data, {"id": id})
        comment = data.get("comment")
        if comment:
            create_comment_and_change_status(request, comment, id)
        return Response(obj)
