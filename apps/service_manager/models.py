from django.db import models


class Apps(models.Model):
    name = models.CharField(max_length=255, unique=True)
    verbose_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.verbose_name or self.name
