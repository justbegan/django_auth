from django.db import models

from apps.profiles.models import Section
from apps.constructor.models import Base_application, Application


class Status(models.Model):
    title = models.CharField("Наименование", max_length=120)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция",
                                related_name='mo_report_statuses')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Mo_report_app(Base_application):
    application = models.ForeignKey(
        Application, on_delete=models.PROTECT, related_name='mo_report_app', verbose_name="Заявление"
    )

    def __str__(self):
        return f"{self.municipal_district} {self.settlement} {self.locality}"

    class Meta:
        verbose_name = "Отчет МО"
        verbose_name_plural = "Отчеты МО"


class Mo_report_schema(models.Model):
    title = models.CharField("Наименование", max_length=120)
    properties = models.JSONField("Properties", default=dict)
    required = models.JSONField("Required", default=list, blank=True, null=True)
    section = models.OneToOneField(Section, on_delete=models.PROTECT, verbose_name="Секция")
    type = models.CharField("Тип", max_length=120)

    class Meta:
        verbose_name = "Схема"
        verbose_name_plural = "Схемы"

    def __str__(self):
        return self.title


class Mo_report_document_type(models.Model):
    title = models.CharField("Наименование", max_length=120)
    required = models.BooleanField("Обязательный")
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип документа"
        verbose_name_plural = "Типы документов"
