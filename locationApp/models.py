from django.db import models
from django_admin_geomap import GeoItem
from django.db.models import Avg

from Location.snippets import name_of_file


class LocationCountry(models.Model):
    country = models.CharField(max_length=50, verbose_name="Страна")

    def __str__(self):
        return self.country

    class Meta:
        verbose_name_plural = "Страна"


class LocationCity(models.Model):
    country = models.ForeignKey(
        LocationCountry, verbose_name="Страна", on_delete=models.CASCADE)
    city = models.CharField(max_length=50, verbose_name="Город")

    def __str__(self):
        return self.city

    class Meta:
        verbose_name_plural = "Город"


class Location(models.Model, GeoItem):
    is_active = models.BooleanField(
        verbose_name="Локация активна", default=False)
    city = models.ForeignKey(LocationCity, verbose_name="Город",
                             on_delete=models.CASCADE, blank=True, null=True)
    district = models.CharField(
        max_length=150, verbose_name="Район/Метро/Улица")
    description = models.TextField(max_length=500, verbose_name="Описание")
    parking = models.BooleanField(default=False, verbose_name="Парковка")
    comfort = models.TextField(max_length=300, verbose_name="Удобства")
    function_less = models.BooleanField(
        default=False, verbose_name="доступность малообильных людей")
    latitude = models.FloatField(
        verbose_name="Широта", )
    longitude = models.FloatField(
        verbose_name="Долгота")
    images = models.ManyToManyField(
        'Images', verbose_name="Картинки для локации")
    category_location = models.ManyToManyField('specialistApp.Category',
                                               related_name="location_cat",
                                               verbose_name="Виды деятельности локации", default=[])

    @property
    def review_avg(self):
        return self.reviews.all().aggregate(Avg("review"))['review__avg']

    @property
    def category(self):
        from specialistApp.models import Category
        from_specialist = Category.objects.filter(specialist__location=self.id).distinct()
        own_category = self.category_location.distinct().all()
        result = from_specialist | own_category
        return own_category

    @property
    def geomap_longitude(self):
        return '' if self.longitude is None else str(self.longitude)

    @property
    def geomap_latitude(self):
        return '' if self.latitude is None else str(self.latitude)

    class Meta:
        verbose_name_plural = "Локации"

    @property
    def country_str(self):
        return str(self.city.country)

    @property
    def city_str(self):
        if self.city:
            return str(self.city)
        return "Не выбран город"

    def __str__(self):
        return "{} {}".format(self.city_str, self.district)


class Images(models.Model):
    folder = "location"
    name = models.CharField(verbose_name="Название Картинки", max_length=55, default="", blank=True)
    images = models.ImageField(
        verbose_name="Картинки для локации", upload_to=name_of_file)

    def save(self, *args, **kwargs):
        if self.name == "":
            self.name = self.images.name.split("_")[-1]
        return super(Images, self).save(*args, **kwargs)

    def __str__(self):
        return self.name if self.name != "" else self.images.name

    class Meta:
        verbose_name_plural = "Фото для локации"
