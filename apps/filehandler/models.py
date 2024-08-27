from django.db import models
import uuid


class File_handler(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField("Описание", blank=True, null=True)
    file = models.FileField("Файл", upload_to="files")

    def __str__(self):
        return f"{self.file}"

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
