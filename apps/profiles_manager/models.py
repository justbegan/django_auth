from django.db import models
from users.serializers import User_serializer
from apps.profiles.serializers import Profile_serializer


class Profiles_manager_app(models.Model):
    STATUS_CH = (
        (1, "Создано"),
        (2, "Выполнено"),
        (3, "Отклонено"),
    )
    text = models.TextField("Текст", blank=True, null=True)
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE,
                                verbose_name="Профиль", blank=True, null=True)
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, verbose_name="Автор")
    section = models.ForeignKey('profiles.Section', on_delete=models.CASCADE, verbose_name="Раздел")
    status = models.IntegerField("Статус", choices=STATUS_CH, default=1)
    municipal_district = models.ForeignKey('locations.Municipal_district',
                                           on_delete=models.SET_NULL, blank=True, null=True)
    settlement = models.ForeignKey('locations.Settlement', on_delete=models.SET_NULL, blank=True, null=True)
    custom_locality = models.TextField("Кастомный населенный пункт", blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = "Заявка на перенос профиля"
        verbose_name_plural = "Заявки на перенос профиля"

    def __str__(self):
        return f"{self.author}"

    def author_obj(self):
        return User_serializer(self.author).data

    def profile_obj(self):
        return Profile_serializer(self.profile).data
