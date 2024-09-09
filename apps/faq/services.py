from rest_framework.views import Request, Response
from copy import deepcopy

from .models import Question, Answer
from .serializer import Question_serializer, Answer_serializer
from apps.constructor.api.services.crud import create, update, get_many, delete
from apps.constructor.api.services.current import get_current_section


def create_question(request: Request):
    data = deepcopy(request.data)
    data['author'] = request.user
    data['section'] = get_current_section(request)
    return Response(create(Question_serializer, data))


def get_all_question_by_section(request: Request):
    return Response(get_many(Question, Question_serializer, {
        "section": get_current_section(request),
        "hide": False
    }))


def update_question(request: Request, id: int):
    data = deepcopy(request.data)
    return Response(update(Question, Question_serializer, data, {"id": id}))


def delete_question(request: Request, id: int):
    return Response(delete(Question, {"id": id}))


def create_answer(request: Request):
    data = deepcopy(request.data)
    data['author'] = request.user
    data['section'] = get_current_section(request)
    return Response(create(Answer_serializer, data))


def update_answer(request: Request, id: int):
    data = deepcopy(request.data)
    return Response(update(Answer, Answer_serializer, data, {"id": id}))


def delete_answer(request: Request, id: int):
    return Response(delete(Answer, {"id": id}))