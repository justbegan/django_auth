from django.db import models


class Municipal_district(models.Model):
    RegionName = models.TextField("Полное наименование")
    RegionNameE = models.CharField("Наименование", max_length=120)
    OKTMO = models.CharField("ОКТМО", max_length=120)
    Population = models.PositiveIntegerField("Население")
    RegOKTMO = models.CharField("ОКТМО региона")
    RegIsNorthern = models.BooleanField("Северный регион")

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

    def __str__(self):
        return self.RegionNameE


class Settlement_type(models.Model):
    title = models.CharField("Наименование")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип поселения"
        verbose_name_plural = "Типы поселений"


class Settlement(models.Model):
    RegID = models.ForeignKey(Municipal_district, on_delete=models.PROTECT, verbose_name="Регион")
    MunicTypeID = models.ForeignKey(Settlement_type, on_delete=models.PROTECT, verbose_name="Тип")
    MunicName = models.TextField("Полное наименование")
    MunicNameE = models.CharField("Наименование", max_length=120)
    Population = models.PositiveIntegerField("Население", null=True, blank=True)
    OKTMO = models.CharField("ОКТМО", max_length=120)
    OKATO = models.CharField("ОКАТО", max_length=120)

    def __str__(self):
        return self.MunicNameE

    class Meta:
        verbose_name = "Поселение"
        verbose_name_plural = "Поселения"


class Locality_type(models.Model):
    title = models.CharField("Наименование")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип населенного пункта"
        verbose_name_plural = "Типы населенных пунктов"


class Locality(models.Model):
    MunicID = models.ForeignKey(Settlement, on_delete=models.PROTECT, verbose_name="Поселение")
    RegID = models.ForeignKey(Municipal_district, on_delete=models.PROTECT, verbose_name="Регион")
    OKTMO = models.CharField("ОКТМО", max_length=120)
    LocName = models.TextField("Полное наименование")
    LocNameE = models.CharField("Наименование", max_length=120)
    LocPopulation = models.PositiveIntegerField("Население")
    LocTypeID = models.ForeignKey(Locality_type, on_delete=models.PROTECT, verbose_name="Тип")

    def __str__(self):
        return self.LocNameE

    class Meta:
        verbose_name = "Населенный пункт"
        verbose_name_plural = "Населенные пункты"