from django.db import models
from django.contrib.auth.models import User

from apps.locations.models import Municipal_district, Settlement, Locality
from apps.profiles.models import Section


class Base_application(models.Model):
    municipal_district = models.ForeignKey(Municipal_district, on_delete=models.PROTECT, verbose_name="Район")
    settlement = models.ForeignKey(Settlement, on_delete=models.PROTECT, verbose_name="Поселение")
    locality = models.ForeignKey(Locality, on_delete=models.PROTECT, verbose_name="Населенный пункт")
    created_at = models.DateTimeField('Дата создания обращения', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    status = models.ForeignKey('Status', on_delete=models.PROTECT, verbose_name="Статус")
    contest = models.ForeignKey('Contest', on_delete=models.PROTECT, verbose_name="Конкурс")
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Пользователь")
    custom_data = models.JSONField("Кастомные поля", default=dict)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")
    documents = models.JSONField("Документы", default=list)

    class Meta:
        abstract = True
