from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username
