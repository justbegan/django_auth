from django.db import models
from django.contrib.contenttypes.models import ContentType

from apps.profiles.models import Section


class Main_table_fields(models.Model):
    TYPE_CH = (
        (1, "Справочник"),
        (2, "Кастомный"),
    )
    title = models.CharField("Наименование", max_length=120)
    field = models.CharField("Транскрипция")
    pos = models.PositiveIntegerField("Позиция", default=100)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция",
                                related_name="table_fields_manager_section")
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, verbose_name="Приложение",
                                     related_name="table_fields_manager_content_type")
    filter = models.BooleanField("Фильтруемый", default=False)
    filter_type = models.IntegerField("Тип", choices=TYPE_CH, blank=True, null=True)
    filter_class = models.ForeignKey(ContentType, on_delete=models.PROTECT, verbose_name="Класс справочника",
                                     related_name="table_fields_manager_filter_type", blank=True, null=True)
    filter_custom_data = models.JSONField("Кастомные данные", blank=True, null=True)
    filter_config = models.JSONField("Настройки поля", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Отображаемемое поле в выбранной таблице"
        verbose_name_plural = "Отображаемые поля в выбранных таблицах"
