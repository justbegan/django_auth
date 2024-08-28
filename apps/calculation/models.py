from django.db import models
from apps.constructor.models import Section


class Formula(models.Model):
    title = models.CharField("Название", max_length=120)
    field = models.CharField("Поле", max_length=120)
    formula = models.CharField("Формула", max_length=120)
    scope = models.FloatField("Сравниваемое значение", default=0)
    hight_value = models.FloatField("Получаемый бал если соответует критерию", default=0)
    coefficent = models.FloatField("Коефицент", default=0)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")

    class Meta:
        verbose_name = "Формула"
        verbose_name_plural = "Формулы"

    def __str__(self):
        return self.title
