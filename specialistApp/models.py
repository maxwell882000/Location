from django.db import models
from Location.settings import AUTH_USER_MODEL
from Location.snippets import name_of_file


class Specialist(models.Model):
    folder = "specialists"
    image = models.ImageField(verbose_name="Фото специалиста", upload_to=name_of_file)
    description = models.CharField(max_length=500)
    user = models.OneToOneField(AUTH_USER_MODEL, verbose_name="Аккаунт специалиста",
                                related_name="user_specialist",
                                on_delete=models.CASCADE)
    is_deactivated = models.BooleanField(default=False, verbose_name="Скрыть карточку специалиста")
    location = models.ForeignKey('locationApp.Location',
                                 verbose_name="Локация специалиста",
                                 on_delete=models.CASCADE
                                 )
    category = models.ManyToManyField('Category',
                                      verbose_name="Виды деятельности специалиста")

    class Meta:
        verbose_name_plural = "Специалист"

    def __str__(self):
        return self.user




class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name="Названия вида деятельности")

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Виды деятельности"
