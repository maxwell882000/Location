from django.db import models


class Plan(models.Model):
    description = models.TextField()
    amount = models.BigIntegerField()
    days = models.IntegerField()

    class Meta:
        verbose_name_plural = "Тарифы"

    def __str__(self):
        return self.description