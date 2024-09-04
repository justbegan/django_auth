from django.db import models
from apps.profiles.models import Section
from apps.locations.models import Settlement_type


class Contest(models.Model):
    NEW = 'new'
    OPENED = 'opened'
    TECH_WORK = 'tech_work'
    CHECK = 'check'
    ON_EXAM = 'on_exam'
    CLOSED = 'closed'

    STATUS = (
        (NEW, 'Новый'),
        (OPENED, 'Идет прием заявок'),
        (TECH_WORK, 'Идут подготовительные работы'),
        (CHECK, 'Идет проверка'),
        (ON_EXAM, 'Идет независимая экспертиза'),
        (CLOSED, 'Конкурс завершен'),
    )
    title = models.CharField("Наименование", max_length=120)
    grant_sum = models.DecimalField("Сумма гранта", max_digits=12, decimal_places=2, default=0.00)
    status = models.CharField("Статус", max_length=120, choices=STATUS, default=NEW)
    contest_types = models.ManyToManyField(Settlement_type, verbose_name="Для кого", help_text="Для кого этот конкурс")
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Конкурс"
        verbose_name_plural = "Конкурсы"


class Status(models.Model):
    title = models.CharField("Наименование", max_length=120)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Project_type(models.Model):
    title = models.CharField("Наименование", max_length=120)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Типология проекта"
        verbose_name_plural = "Типологии проектов"


class Document_type(models.Model):
    title = models.CharField("Наименование", max_length=120)
    required = models.BooleanField("Обязательный")
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип документа"
        verbose_name_plural = "Типы документов"
