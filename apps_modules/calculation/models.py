from django.db import models
from apps.constructor.models import Section


code_template = """#python!
# result - пустой dict
# self.get_financing_settlement_budget() - Бюджет поселения (муниципального района)
# self.get_financing_people() - Население (поступления от жителей)
# self.get_financing_sponsors() - Спонсоры
# self.get_financing_republic_grant() - Субсидия из бюджета Республики Саха (Якутия)
# self.total_price() - Общая сумма
# key - названия поля
# value - значение поля
result[key] =
"""


class Formula(models.Model):
    title = models.CharField("Название", max_length=120)
    description = models.TextField("Описание", blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")
    code = models.TextField("Код", default=code_template)

    class Meta:
        verbose_name = "Формула"
        verbose_name_plural = "Формулы"

    def __str__(self):
        return self.title
