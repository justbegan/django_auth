from django.db import models
from django.contrib.auth.models import User


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

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
