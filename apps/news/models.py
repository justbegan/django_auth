from django.db import models
from apps.profiles.models import Section


class News(models.Model):
    title = models.TextField("Наименование")
    text = models.TextField("Текст")
    hide = models.BooleanField("Скрытый", default=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Секция')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return f"{self.title}"
