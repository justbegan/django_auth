from django.db import models
from apps.profiles.models import Section
from apps.constructor.models import Base_application, Base_status, Application, Base_schema


class Status(Base_status):
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Meeting_app(Base_application):
    status = models.ForeignKey('Status', on_delete=models.PROTECT, verbose_name="Статус",
                               related_name='%(class)s_set')
    application = models.ForeignKey(
        Application, on_delete=models.SET_NULL, verbose_name="Заявка", null=True, blank=True
    )

    def __str__(self):
        return f"{self.municipal_district} {self.settlement} {self.locality}"

    class Meta:
        verbose_name = "Собрание"
        verbose_name_plural = "Собрания"

    def get_selected_project(self):
        try:
            obj = self.custom_data.get('projects_under_discussion')
            return max(obj, key=lambda x: x['voter_count'])['project_title']
        except Exception:
            return None


class Meeting_schema(Base_schema):
    class Meta:
        verbose_name = "Схема"
        verbose_name_plural = "Схемы"

    def __str__(self):
        return self.title


class Meeting_document_type(models.Model):
    title = models.CharField("Наименование", max_length=120)
    required = models.BooleanField("Обязательный")
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип документа"
        verbose_name_plural = "Типы документов"
