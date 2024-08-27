from django.db import models
from django.contrib.auth.models import User
from apps.locations.models import Municipal_district, Settlement, Locality
from apps.profiles.models import Section


class Contest(models.Model):
    title = models.CharField("Наименование", max_length=120)
    active = models.BooleanField("Активность", default=True)
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


class Application(models.Model):
    title = models.TextField("Наименование проекта")
    municipal_district = models.ForeignKey(Municipal_district, on_delete=models.PROTECT, verbose_name="Район")
    settlement = models.ForeignKey(Settlement, on_delete=models.PROTECT, verbose_name="Поселение")
    locality = models.ForeignKey(Locality, on_delete=models.PROTECT, verbose_name="Населенный пункт")
    project_type = models.ForeignKey(Project_type, on_delete=models.PROTECT, verbose_name="Типология проекта")
    created_at = models.DateTimeField('Дата создания обращения', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    contest = models.ForeignKey(Contest, on_delete=models.PROTECT, verbose_name="Конкурс")
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Пользователь")
    custom_data = models.JSONField("Кастомные поля", default=dict)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


class History(models.Model):
    application = models.ForeignKey(Application, on_delete=models.PROTECT, verbose_name="Заявка")
    created_at = models.DateTimeField('Дата создания обращения', auto_now_add=True)
    text = models.TextField("Текст")
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Пользователь")

    class Meta:
        verbose_name = "История"
        verbose_name_plural = "Истории"


class Comments(models.Model):
    application = models.ForeignKey(Application, on_delete=models.PROTECT, verbose_name="Заявка")
    text = models.TextField("Текст")
    created_at = models.DateTimeField('Дата создания обращения', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Коммент"
        verbose_name_plural = "Комменты"


class Document_type(models.Model):
    title = models.CharField("Наименование", max_length=120)
    requirements = models.BooleanField("Обязательный")
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип документа"
        verbose_name_plural = "Типы документов"


class Document(models.Model):
    document_type = models.ForeignKey(Document_type, on_delete=models.PROTECT, verbose_name="Тип")
    file_urls = models.JSONField("Ссылки на файлы", default=list)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"


class Schema(models.Model):
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