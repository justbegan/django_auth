from rest_framework.views import Request, Response
from copy import deepcopy

from .models import Question
from .serializer import Question_serializer
from services.crud_services import Base_crud
from services.current import get_current_section


def create_question(request: Request):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request).id
    return Response(Base_crud.create(Question_serializer, data))


def get_all_question_by_section(request: Request):
    return Response(Base_crud.get_many(Question, Question_serializer, {
        "section": get_current_section(request),
        "hide": False
    }))


def update_question(request: Request, id: int):
    data = deepcopy(request.data)
    data['section'] = get_current_section(request).id
    return Response(Base_crud.update(Question, Question_serializer, data, {"id": id}))


def delete_question(request: Request, id: int):
    return Response(Base_crud.delete(Question, {"id": id}))
