from django.db import models


class Document(models.Model):
    title = models.TextField("Наименовение")
    description = models.TextField("Описание")
    date = models.DateField("Дата")
    file_url = models.CharField("ссылка")
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return f"{self.title}"
