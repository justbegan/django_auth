from django.db import models
from django.contrib.auth.models import User
from .services.services import get_all_contest_from_fast_api as all_contests


class Roles(models.Model):
    title = models.TextField("Название")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Профиль")
    role = models.ForeignKey(Roles, on_delete=models.PROTECT, verbose_name="Роль")
    contest = models.CharField("Конкурс", max_length=120, choices=all_contests().items())

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
