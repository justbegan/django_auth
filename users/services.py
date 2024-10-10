from rest_framework.request import Request
from rest_framework.views import Response, status
from django.core.mail import send_mail
import random
from django.conf import settings
import string

from users.models import CustomUser
from .serializers import User_serializer, User_put_serializer
from services.crud import update, get, create, get_many, patch
from apps.constructor.services.current import get_current_section
from .models import VerificationCode


def get_user(request):
    return Response(get(CustomUser, User_serializer, {"id": request.user.id}))


def get_user_id(request: Request, user_id: int):
    return Response(get(CustomUser, User_serializer, {"id": user_id}))


def update_user(request: Request, user_id: int):
    data = request.data
    user = update(CustomUser, User_put_serializer, data, {"id": user_id})
    return Response(user)


def create_user(request: Request):
    data = request.data
    data['is_active'] = False
    return Response(create(User_serializer, data))


def get_all_users(request: Request):
    users = get_many(CustomUser, User_serializer, {"profile__section": get_current_section(request)})
    return Response(users)


def get_new_users(request: Request):
    users = get_many(CustomUser, User_serializer,
                     {"profile__section": get_current_section(request), "is_active": False})
    return Response(users)


def repeat_email(request: Request):
    email = request.data['email']
    try:
        user = CustomUser.objects.get(email=email)
    except Exception:
        return Response(
            {"success": False, "text": "Пользователь с таким e-mail не найден"},
            status=status.HTTP_404_NOT_FOUND
        )
    VerificationCode.objects.filter(user=user).delete()
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    VerificationCode.objects.create(user=user, code=code)

    send_mail(
        'Подтверждение регистрации',
        f'Ваш код подтверждения: {code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    return Response({"success": True, "text": "Код повторно отправлен"})


def generate_password():
    password_length = 9
    password = ''.join(random.choices(
        string.ascii_letters + string.digits + string.punctuation, k=password_length)
    )
    return password


def recover_password(request: Request):
    email = request.data['email']
    try:
        user = CustomUser.objects.get(email=email)
    except Exception:
        return Response(
            {"success": False, "text": "Пользователь с таким e-mail не найден"},
            status=status.HTTP_404_NOT_FOUND
        )
    new_pass = generate_password()
    user.set_password(new_pass)
    user.is_active = True
    user.save()
    send_mail(
        'Востановления доступа',
        f'Ваш новый пароль: {new_pass}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    return Response({"success": True, "text": "Пароль сброшен. Новый пароль сгенерирован, проверьте свой e-mail."})


def patch_user(request: Request, id: int):
    return Response(patch(CustomUser, User_serializer, request.data, {'id': id}))
