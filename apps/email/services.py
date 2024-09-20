from django.core.mail import send_mail
from django.conf import settings


def send_simple_email():
    send_mail(
        'Subject of the email',  # Тема письма
        'Here is the message body.',  # Тело письма
        settings.DEFAULT_FROM_EMAIL,  # Отправитель
        ['justbegan@mail.ru'],  # Получатели
        fail_silently=False,  # Если установить в True, ошибки при отправке будут игнорироваться
    )
