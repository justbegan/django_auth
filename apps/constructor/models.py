from django.db import models
from django.contrib.auth.models import User
from apps.locations.models import Municipal_district, Settlement, Locality
from apps.profiles.models import Section
from apps.calculation.models import Formula
from .classificators_models import Project_type, Status, Contest, Document_type


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

    def point_calculation(self):
        result = {}
        try:
            formulas = Formula.objects.filter(section=self.section)
            for f in formulas:
                try:
                    exec(f.code)
                except:
                    pass
        except:
            return result
        return result

    def get_financing_settlement_budget(self) -> float:
        """
            Бюджет поселения (муниципального района)
        """
        return self.custom_data.get("financing_settlement_budget", 0.0)

    def get_financing_people(self) -> float:
        """
            Население (поступления от жителей)
        """
        return self.custom_data.get("financing_people", 0.0)

    def get_financing_sponsors(self) -> float:
        """
            Спонсоры (денежные поступления от юр.лиц, инд.предпринимателей и т.д.)
        """
        return self.custom_data.get("financing_sponsors", 0.0)

    def get_financing_republic_grant(self) -> float:
        """
            Субсидия из бюджета Республики Саха (Якутия)
        """
        return self.custom_data.get("financing_republic_grant", 0.0)

    def total_price(self):
        return sum(
            [
                self.get_financing_settlement_budget(),
                self.get_financing_people(),
                self.get_financing_sponsors(),
                self.get_financing_republic_grant()
            ]
        )


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


class Document(models.Model):
    application = models.ForeignKey(Application, on_delete=models.PROTECT, verbose_name="Заявка")
    document_type = models.ForeignKey(Document_type, on_delete=models.PROTECT, verbose_name="Тип")
    file_urls = models.JSONField("Ссылки на файлы", default=list)

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


class Main_table_fields(models.Model):
    title = models.CharField("Наименование", max_length=120)
    field = models.CharField("Транскрипция")
    pos = models.PositiveIntegerField("Позиция", default=100)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Секция")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Отображаемое значение в главной таблице"
        verbose_name = "Отображаемые значения в главной таблице"
