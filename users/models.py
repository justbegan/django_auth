from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history.models import HistoricalRecords

from apps.profiles.models import Profile
from apps.profiles.serializers import Profile_serializer


class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    current_section = models.ForeignKey('profiles.Section', on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name="Текущая секция")
    history = HistoricalRecords("История")

    def __str__(self):
        return self.username

    def profiles(self):
        obj = Profile.objects.filter(user=self).all()
        return Profile_serializer(obj, many=True).data
