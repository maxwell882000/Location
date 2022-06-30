from django.db import models


class Confidential(models.Model):
    header = models.CharField(max_length=100, verbose_name="Загаловок")
    body = models.TextField(verbose_name="Описание правил")

    class Meta:
        verbose_name_plural = "Правила конфидециальности"

    def __str__(self) -> str:
        return "Конфедициальность"


class SaleText(models.Model):
    header = models.CharField(max_length=100, verbose_name="Загаловок")
    body = models.TextField(verbose_name="Описание правил")

    class Meta:
        verbose_name_plural = "Правила покупки услуг"

    def __str__(self) -> str:
        return "Покупка услуг"


class Instructions(models.Model):
    header = models.CharField(max_length=100, verbose_name="Загаловок")
    body = models.TextField(verbose_name="Описание правил")

    class Meta:
        verbose_name_plural = "Инструкции"

    def __str__(self) -> str:
        return "Инструкции"
