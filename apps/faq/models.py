from django.db import models
from django.contrib.auth.models import User

from apps.profiles.models import Section


class Question(models.Model):
    text = models.TextField("Вопрос")
    hide = models.BooleanField("Скрытый", default=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор")
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Раздел")
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопрос"

    def __str__(self):
        return self.text

    def get_answer(self):
        from .serializer import Answer_serializer
        try:
            return Answer_serializer(Answer.objects.get(question=self)).data
        except Exception:
            return {}


class Answer(models.Model):
    question = models.OneToOneField(Question, verbose_name="Вопрос", on_delete=models.PROTECT)
    text = models.TextField("Вопрос")
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор")
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.text
