from django.db import models
from apps.profiles.models import Section


class Report(models.Model):
    title = models.CharField("Наименование", max_length=120)
    url = models.URLField("Ссылка на отчет")
    description = models.TextField("Описание", blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Раздел")

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"

    def __str__(self):
        return self.title
