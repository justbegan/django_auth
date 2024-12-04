from django.db import models
from users.models import CustomUser


class Ad(models.Model):
    text = models.TextField("Текст")
    start_date = models.DateTimeField("Время начала")
    end_date = models.DateTimeField("Время окончания")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return f"{self.text}"
