from django.db import models

from Location.snippets import name_of_file


class Add(models.Model):
    folder = "adds"
    image = models.ImageField(verbose_name="Картинка для Рекламы", upload_to=name_of_file)
    link = models.CharField(verbose_name="Линк для рекламы", max_length=255)

    class Meta:
        verbose_name_plural = "Реклама"

    def __str__(self):
        return self.link
