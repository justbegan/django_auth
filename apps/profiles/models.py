from django.db import models
from django.contrib.contenttypes.models import ContentType

from apps.locations.models import Municipal_district, Settlement, Locality
from apps.module_manager.models import Apps


class Section(models.Model):
    title = models.CharField("Секция", max_length=120)
    logo = models.CharField("Ссылка на лого", blank=True, null=True, max_length=200)
    header = models.TextField("Заголовок", blank=True, null=True)
    modules = models.ManyToManyField(Apps, verbose_name="Модули", blank=True)
    tech_name = models.CharField("Тех. название", max_length=120)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"

    def modules_data(self):
        return self.modules.all().values()


class Roles(models.Model):
    title = models.TextField("Название")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"


class Profile_type(models.Model):
    title = models.CharField("Наименование", max_length=120)
    abbreviation = models.CharField("Описание", max_length=120)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип профиля"
        verbose_name_plural = "Типы профилей"


class Profile(models.Model):
    title = models.CharField("Имя", max_length=320)
    role = models.ForeignKey(Roles, on_delete=models.PROTECT, verbose_name="Роль")
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name="Раздел", blank=True, null=True)
    municipal_district = models.ForeignKey(
        Municipal_district, on_delete=models.PROTECT, verbose_name="Район", blank=True, null=True
    )
    settlement = models.ForeignKey(
        Settlement, on_delete=models.PROTECT, verbose_name="Поселение", blank=True, null=True
    )
    locality = models.ForeignKey(
        Locality, on_delete=models.PROTECT, verbose_name="Населенный пункт", blank=True, null=True
    )
    profile_type = models.ForeignKey(Profile_type, on_delete=models.PROTECT, verbose_name="Тип профиля", blank=True,
                                     null=True)
    user = models.ForeignKey('users.CustomUser', on_delete=models.PROTECT, blank=True, null=True)
    allowed_number_projects = models.PositiveIntegerField("Допустимое количество проектов", default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def get_modules(self):
        try:
            return self.section.modules.all().values()
        except Exception:
            return {}


class Role_handler(models.Model):
    model = models.ForeignKey(ContentType, verbose_name="Модель", on_delete=models.PROTECT)
    roles = models.ManyToManyField(Roles, verbose_name="Роли")
    section = models.ForeignKey(
        Section, on_delete=models.PROTECT, verbose_name="Раздел"
    )

    def __str__(self):
        return f"{self.model}"

    class Meta:
        verbose_name = "Доступ к методу"
        verbose_name_plural = "Доступы к методам"
