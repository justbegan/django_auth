from django.db import models
import logging
from simple_history.models import HistoricalRecords
from django.contrib.contenttypes.models import ContentType
# from decimal import Decimal

from apps.profiles.models import Section, Profile, Roles
from apps.locations.models import Municipal_district, Settlement, Locality, District_type

logger = logging.getLogger('django')


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
    district_type = models.ManyToManyField(District_type, verbose_name="Для кого", help_text="Для кого этот конкурс")
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")
    year = models.PositiveIntegerField("Год проведения")
    history = HistoricalRecords("История")

    def __str__(self):
        return f"{self.title}|{self.year}|{self.section}"

    class Meta:
        verbose_name = "Конкурс"
        verbose_name_plural = "Конкурсы"


class Base_status(models.Model):
    title = models.CharField("Наименование", max_length=120)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция",
                                related_name='%(app_label)s_set')
    tech_name = models.CharField("Тех. название", max_length=30)
    roles = models.ManyToManyField(Roles, related_name='%(app_label)s_set', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Status(Base_status):
    title = models.CharField("Наименование", max_length=120)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция",
                                related_name='constuctor_statuses')
    tech_name = models.CharField("Тех. название", max_length=30)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Project_type(models.Model):
    title = models.CharField("Наименование", max_length=300)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Типология проекта"
        verbose_name_plural = "Типологии проектов"


class Document_type(models.Model):
    title = models.TextField("Наименование")
    required = models.BooleanField("Обязательный")
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип документа"
        verbose_name_plural = "Типы документов"


class Base_application(models.Model):
    municipal_district = models.ForeignKey(Municipal_district, on_delete=models.PROTECT, verbose_name="Район",
                                           related_name='%(class)s_set')
    settlement = models.ForeignKey(Settlement, on_delete=models.PROTECT, verbose_name="Поселение",
                                   related_name='%(class)s_set', blank=True, null=True)
    locality = models.ForeignKey(Locality, on_delete=models.PROTECT, verbose_name="Населенный пункт",
                                 related_name='%(class)s_set', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания обращения', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    contest = models.ForeignKey(Contest, on_delete=models.PROTECT, verbose_name="Конкурс",
                                related_name='%(class)s_set')
    author = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name="Пользователь",
                               related_name='%(class)s_set')
    custom_data = models.JSONField("Кастомные поля", default=dict)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция",
                                related_name='%(class)s_set')
    documents = models.JSONField("Документы", default=list)

    class Meta:
        abstract = True


class Application(Base_application):
    status = models.ForeignKey('Status', on_delete=models.PROTECT, verbose_name="Статус",
                               related_name='%(class)s_set')
    title = models.TextField("Наименование проекта")
    project_type = models.ForeignKey(
        Project_type, on_delete=models.PROTECT, verbose_name="Типология проекта", blank=True, null=True
    )
    history = HistoricalRecords("История")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def get_lat_lon(self):
        try:
            return {
                "latitude": self.locality.Latitude,
                "longitude": self.locality.Longitude
            }
        except Exception:
            return {}

    def get_project_problem(self):
        """
        Цель проекта
        """
        return self.custom_data.get("project_problem", "")


class Base_schema(models.Model):
    title = models.CharField("Наименование", max_length=120)
    properties = models.JSONField("Properties", default=dict)
    required = models.JSONField("Required", default=list, blank=True, null=True)
    section = models.OneToOneField(Section, on_delete=models.PROTECT, verbose_name="Секция")
    contests = models.ManyToManyField(Contest, verbose_name="Конкурсы", blank=True)
    type = models.CharField("Тип", max_length=120)

    class Meta:
        abstract = True


class Schema(Base_schema):
    class Meta:
        verbose_name = "Схема"
        verbose_name_plural = "Схемы"

    def __str__(self):
        return self.title


class Main_table_fields(models.Model):
    title = models.CharField("Наименование", max_length=120)
    field = models.CharField("Транскрипция")
    pos = models.PositiveIntegerField("Позиция", default=100)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, verbose_name="Приложение")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Отображаемое значение в главной таблице"
        verbose_name_plural = "Отображаемые значения в главной таблице"


class Custom_validation(models.Model):
    code_template = """#python!
# imported models Application, Profile
current_user = request.user
current_contest = get_current_contest(request)
profile_type = Profile.objects.get(user__id=current_user.id).profile_type
"""

    title = models.CharField("Наименование", max_length=120)
    code = models.TextField("Код", default=code_template)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кастомное валидирование"
        verbose_name_plural = "Кастомные валидации"


class Calculated_fields(models.Model):
    FIELD_TYPE_CHOICES = (
        (1, "IntegerField"),
        (2, "CharField"),
        (3, "FloatField"),
        (4, "DecimalField"),
    )
    title = models.CharField("Наименование", max_length=120)
    code = models.TextField("Код")
    field_type = models.IntegerField("Тип поля", choices=FIELD_TYPE_CHOICES, default=2)
    func_type = models.IntegerField("Тип метода", choices=((1, "annotate"), (2, "aggregate"),), default=1)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    use_sum = models.BooleanField("Использовать SUM", default=False)
    contest = models.ManyToManyField(Contest, verbose_name="Конкурс", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Вычисляемое поле"
        verbose_name_plural = "Вычисляемые поля"
