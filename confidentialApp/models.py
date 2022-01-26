from email import header
from statistics import mode
from django.db import models

class Confidential(models.Model):
    header = models.CharField(max_length=100, verbose_name="Загаловок")
    body = models.TextField(verbose_name="Описание правил")

    class Meta:
        verbose_name_plural = "Правила конфидециальности"
