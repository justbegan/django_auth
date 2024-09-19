from django.db import models
from django.contrib.auth.models import User

from apps.profiles.models import Section


class Letter(models.Model):
    text = models.TextField("Текст")
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор")
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Раздел")
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"

    def __str__(self):
        return f"{self.author}"
