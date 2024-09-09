from django.db import models
from django.contrib.auth.models import User

from apps.constructor.models import Application


class History(models.Model):
    application = models.ForeignKey(
        Application, on_delete=models.PROTECT, verbose_name="Заявка", related_name="history_application")
    diff = models.JSONField("Отличия", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор", related_name="history_author")
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = "История"
        verbose_name_plural = "Истории"

    def __str__(self):
        return self.text
