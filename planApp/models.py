from django.db import models


class Plan(models.Model):
    description = models.TextField()
    amount = models.BigIntegerField()

    class Meta:
        verbose_name_plural = "Тарифы"
