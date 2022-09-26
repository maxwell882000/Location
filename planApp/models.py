from django.db import models


class Plan(models.Model):
    description = models.TextField(verbose_name="Описание тарифа")
    amount = models.BigIntegerField(verbose_name="Количество денег в рублях")
    days = models.IntegerField(verbose_name="На какое количество дней активируеться аккаунт")

    class Meta:
        verbose_name_plural = "Тарифы"

    def __str__(self):
        return self.description