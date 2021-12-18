from django.db import models

# Create your models here.
from Location.snippets import name_of_file


class CommonIcon(models.Model):
    folder = "icons"
    icon = models.ImageField(
        verbose_name="Иконки", upload_to=name_of_file)

    class Meta:
        verbose_name_plural = "Общие иконки"

    def __str__(self):
        return "Иконка №{}".format(self.id)


class CommonLogo(models.Model):
    folder = "logo"
    logo = models.ImageField(
        verbose_name="Картинки для локации", upload_to=name_of_file)

    class Meta:
        verbose_name_plural = "Лого"

    def __str__(self):
        return "Лого №{}".format(self.id)
