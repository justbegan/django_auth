from rest_framework.request import Request
from rest_framework.views import Response
from django.core.mail import send_mail
import random
from django.conf import settings

from users.models import CustomUser
from .serializers import User_serializer
from services.crud import update, get, create, get_many
from apps.constructor.services.current import get_current_section
from apps.profiles.models import Profile
from .models import VerificationCode


def get_user(request):
    return Response(get(CustomUser, User_serializer, {"id": request.user.id}))


def get_user_id(request: Request, user_id: int):
    return Response(get(CustomUser, User_serializer, {"id": user_id}))


def update_user(request: Request, user_id: int):
    data = request.data
    user = update(CustomUser, User_serializer, data, {"id": user_id})
    return Response(user)


def create_user(request: Request):
    data = request.data
    data['is_active'] = False
    municipal_district_id = data['municipal_district_id']
    settlement_id = data['settlement_id']
    locality_id = data['locality_id']
    profile = Profile.objects.get(
        municipal_district=municipal_district_id,
        settlement=settlement_id,
        locality=locality_id
    )
    data['profile'] = profile.id
    return Response(create(User_serializer, data)['id'])


def get_all_users(request: Request):
    users = get_many(CustomUser, User_serializer, {"profile__section": get_current_section(request)})
    return Response(users)


def get_new_users(request: Request):
    users = get_many(CustomUser, User_serializer,
                     {"profile__section": get_current_section(request), "is_active": False})
    return Response(users)


def repeat_email(request: Request):
    email = request.data['email']
    user = CustomUser.objects.get(email=email)
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
    return Response({"success": True})
