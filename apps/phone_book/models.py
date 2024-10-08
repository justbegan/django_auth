from django.db import models
from apps.profiles.models import Section
from django.core.validators import RegexValidator


class Phone_book(models.Model):
    phoneNumberRegex = RegexValidator(regex=r"^[\d\-\+]+$")
    fio = models.CharField("ФИО", max_length=100)
    position = models.TextField("Должность")
    description = models.TextField("Описание", blank=True, null=True)
    phone = models.CharField("Телефон", validators=[phoneNumberRegex], max_length=30)
    ip_phone = models.CharField("ip Телефон", validators=[phoneNumberRegex], max_length=30, blank=True, null=True)
    email = models.EmailField("Email", blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name="Раздел", on_delete=models.PROTECT)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = "Телефонный справочник"
        verbose_name_plural = "Телефонные справочники"
