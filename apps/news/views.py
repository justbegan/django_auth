from rest_framework.views import APIView, Request

from .services import get_all_news, create_news, update_news, delete_news, get_new_by_id


class News_main(APIView):
    def get(self, request: Request):
        """
        Получить все новости
        """
        return get_all_news(request)

    def post(self, request: Request):
        return create_news(request)


class News_detail(APIView):
    def get(self, request: Request, id: int):
        return get_new_by_id(request, id)

    def put(self, request: Request, id: int):
        return update_news(request, id)

    def delete(self, request: Request, id: int):
        return delete_news(request, id)
