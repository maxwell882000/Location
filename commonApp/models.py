from django.db import models
from django.db.models.enums import Choices

# Create your models here.
from Location.snippets import name_of_file

CHOICES = (
    (0, 'Меню'),
    (1, 'Виды деятельности'),
    (2, 'Специалисты'),
    (3, 'Личный кабинет пользователя')
)


class CommonIcon(models.Model):
    folder = "icons"
    icon = models.ImageField(
        verbose_name="Иконки", upload_to=name_of_file)
    type = models.IntegerField(choices=CHOICES, default=0, unique=True)

    class Meta:
        verbose_name_plural = "Общие иконки"

    def __str__(self):
        return CHOICES[self.type][1]


class TempImage(models.Model):
    folder = "specialists"
    temp = models.ImageField(verbose_name="Темп фото", upload_to=name_of_file)

    @property
    def temp_url(self):
        return self.temp.url
class CommonLogo(models.Model):
    folder = "logo"
    logo = models.ImageField(
        verbose_name="Картинки для локации", upload_to=name_of_file)

    class Meta:
        verbose_name_plural = "Лого"

    def __str__(self):
        return "Лого №{}".format(self.id)
