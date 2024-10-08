from rest_framework.views import Response
from rest_framework.request import Request
import requests

from ..models import Api_getaway_mappping, Remaining_paths
from apps.profiles.models import Profile
from django.http import HttpResponse


def report_service(url: str) -> bool:
    try:
        url = url.split("/")[0]
        if url == 'report':
            return True
        return False
    except Exception:
        return False


def make_a_request(request: Request, path: str):
    """Сделать запрос на микросервис"""
    response = requests.request(
        **get_request_param(request, path)
    )
    if report_service(path):
        return HttpResponse(response)
    else:
        return Response(response.json(), status=response.status_code)


def get_request_param(request: Request, path: str) -> dict:
    """Параметры запроса"""
    param = {
        "method": request.method,
        "url": get_url(request, path),
        "headers": validate_header(request.headers),
        "params": request.GET
    }
    if path == 'contest_constructor/files/upload-doc':
        param['files'] = request.data
    else:
        param['json'] = request.data
    return param


def validate_header(headers):
    """
    Удаление из header не валидные параметры
    """
    not_valid_parameter = ['Content-Length', 'Content-Type']
    h = {key: value for key, value in dict(headers).items() if key not in not_valid_parameter}
    return h


def get_url(request: Request, path: str):
    """
    Формировать url запроса
    """
    parts = path.split('/', 1)
    microservice_name = parts[0]
    remaining_path = parts[1] if len(parts) > 1 else ''
    check_path(request, remaining_path)
    try:
        microservice_path = Api_getaway_mappping.objects.get(name=microservice_name).url
    except Exception as e:
        raise Exception(e)

    microservice_url = f'{microservice_path}/{remaining_path}'
    return microservice_url


def check_path(request: Request, path: str) -> bool:
    """
    проверка доп. маршрута
    """
    try:
        r_path = Remaining_paths.objects.get(name=path)
    except Exception:
        return True
    if r_path:
        role = r_path.role
        user_role = Profile.objects.get(user=request.user).role
        if user_role.title == 'admin':
            return True
        elif role == user_role:
            return True
        else:
            raise Exception("Forbiden 403")
