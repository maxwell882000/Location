from django.db import models
from django_admin_geomap import GeoItem

from Location.snippets import name_of_file


class LocationCountry(models.Model):
    country = models.CharField(max_length=50, verbose_name="Страна")

    def __str__(self):
        return self.country

    class Meta:
        verbose_name_plural = "Страна"


class LocationCity(models.Model):
    country = models.ForeignKey(LocationCountry, verbose_name="Страна", on_delete=models.CASCADE)
    city = models.CharField(max_length=50, verbose_name="Город")

    def __str__(self):
        return self.city

    class Meta:
        verbose_name_plural = "Город"


class Location(models.Model, GeoItem):
    is_active = models.BooleanField(verbose_name="Локация активна", default=True)
    city = models.ForeignKey(LocationCity, verbose_name="Город", on_delete=models.CASCADE)
    district = models.CharField(max_length=150, verbose_name="Район")
    description = models.TextField(max_length=500, verbose_name="Описание")
    latitude = models.FloatField(
        verbose_name="Широта", )
    longitude = models.FloatField(
        verbose_name="Долгота")
    images = models.ManyToManyField('Images', verbose_name="Картинки для локации", )

    @property
    def geomap_longitude(self):
        return '' if self.longitude is None else str(self.longitude)

    @property
    def geomap_latitude(self):
        return '' if self.latitude is None else str(self.latitude)

    class Meta:
        verbose_name_plural = "Локации"

    def __str__(self):
        return "{} {} {}".format(self.city.country, self.city, self.district)


class Images(models.Model):
    folder = "location"
    images = models.ImageField(verbose_name="Картинки для локации", upload_to=name_of_file)

    def __str__(self):
        return self.images.name

    class Meta:
        verbose_name_plural = "Фото для локации"
