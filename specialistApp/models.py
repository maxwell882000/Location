from django.db import models
from django.db.models import Avg

from Location.settings import AUTH_USER_MODEL
from Location.snippets import name_of_file
import locationApp.models


class Specialist(models.Model):
    folder = "specialists"
    image = models.ImageField(verbose_name="Фото специалиста", upload_to=name_of_file)

    description = models.TextField(verbose_name="Описание")

    user = models.OneToOneField(AUTH_USER_MODEL, verbose_name="Аккаунт специалиста",
                                related_name="user_specialist",
                                on_delete=models.CASCADE)
    plan = models.ForeignKey("planApp.Plan", related_name='specialist',
                             null=True,
                             blank=True,
                             verbose_name="Тариф специалиста",
                             on_delete=models.CASCADE)
    days_activated = models.IntegerField(default=0, verbose_name="Количество дней про аккаунта")
    custom_location = models.TextField(verbose_name="Ручная локация",
                                       null=True,
                                       blank=True,
                                       max_length=255)
    # location_many = models.ManyToManyField('locationApp.Location',
    #                                        verbose_name="Локации")
    location = models.ForeignKey('locationApp.Location',
                                 related_name='specialist',
                                 null=True,
                                 blank=True,
                                 verbose_name="Локация специалиста",
                                 on_delete=models.CASCADE
                                 )
    category = models.ManyToManyField('Category',
                                      verbose_name="Виды деятельности специалиста")

    @property
    def is_deactivated(self):
        return self.days_activated == 0

    @property
    def review_avg(self):
        return self.reviews.all().aggregate(Avg("review"))['review__avg']

    @property
    def is_auto_payment(self):
        return self.order_status is not None and self.order_status.bindingId is not None

    class Meta:
        verbose_name_plural = "Специалист"

    def __str__(self):
        return self.user.fullname


class Category(models.Model):
    folder = "category"
    image = models.ImageField(verbose_name="Фото специалиста", upload_to=name_of_file)
    category_name = models.CharField(max_length=100, verbose_name="Названия вида деятельности")
    description = models.TextField(max_length=500, verbose_name="Описание для вида деятельности")
    is_active = models.BooleanField(default=True, verbose_name="Актививация видов деятельности")

    def __str__(self):
        return self.category_name

    @property
    def location(self):
        return self.location_cat.distinct() | \
               locationApp.models.Location.objects.filter(specialist__category=self.id).distinct()

    class Meta:
        verbose_name_plural = "Виды деятельности"
