from rest_framework.views import Request, APIView

from .services import (get_all_question_by_section, create_question, update_question, delete_question,
                       create_answer, update_answer, delete_answer)


class Question_main(APIView):
    def get(self, request: Request):
        return get_all_question_by_section(request)

    def post(self, request: Request):
        return create_question(request)


class Question_detail(APIView):
    def put(self, request: Request):
        return update_question(request)

    def delete(self, request: Request):
        return delete_question(request)


class Answer_main(APIView):
    def post(self, request: Request):
        return create_answer(request)


class Answer_detail(APIView):
    def put(self, request: Request, id: int):
        return update_answer(request)

    def delete(self, request: Request, id: int):
        return delete_answer(request)
