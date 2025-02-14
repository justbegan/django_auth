from django.http import JsonResponse
from users.models import CustomUser
from django.utils import timezone


class Process500:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception):
        return JsonResponse(
            {
                "message": str(exception)
            },
            status=500
        )


class Register_last_request:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = CustomUser.objects.get(id=request.user.id)
            user.last_activity = timezone.now()
            user.save()
        return self._get_response(request)
