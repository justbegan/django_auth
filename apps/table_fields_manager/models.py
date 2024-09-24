from django.db import models
from django.contrib.contenttypes.models import ContentType

from apps.profiles.models import Section


class Main_table_fields(models.Model):
    title = models.CharField("Наименование", max_length=120)
    field = models.CharField("Транскрипция")
    pos = models.PositiveIntegerField("Позиция", default=100)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция",
                                related_name="table_fields_manager_section")
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, verbose_name="Приложение",
                                     related_name="table_fields_manager_content_type")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Отображаемемое поле в выбранной таблице"
        verbose_name_plural = "Отображаемые поля в выбранных таблицах"
