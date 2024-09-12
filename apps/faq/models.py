from django.db import models
from django.contrib.auth.models import User

from apps.profiles.models import Section


class Question(models.Model):
    question = models.TextField("Вопрос")
    answer = models.TextField("Ответ")
    hide = models.BooleanField("Скрытый", default=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор")
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Раздел")
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.question
