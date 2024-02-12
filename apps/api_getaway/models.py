from django.db import models
from apps.profiles.models import Roles


class Api_getaway_mappping(models.Model):
    name = models.TextField("Название микросервиса")
    url = models.URLField("Url")
    description = models.TextField("Описание", blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Маршрут апи"
        verbose_name_plural = "Маршруты апи"


class Remaining_paths(models.Model):
    name = models.TextField("Название")
    role = models.ForeignKey(Roles, verbose_name="Роль", on_delete=models.PROTECT)
    service = models.ForeignKey(Api_getaway_mappping, verbose_name="Сервис", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Приватный путь"
        verbose_name_plural = "Приватные пути"
