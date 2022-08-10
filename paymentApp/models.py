from pyexpat import model
from django.db import models

# Create your models here.
from planApp.models import Plan
from specialistApp.models import Specialist


class OrderUnique(models.Model):
    order_user = models.ForeignKey(Specialist, related_name="order_unique", on_delete=models.CASCADE)
    orderId = models.CharField(max_length=255, null=True, blank=True)  # store when
    amount = models.BigIntegerField()


class OrderStatus(models.Model):
    order = models.OneToOneField(Specialist, on_delete=models.CASCADE, related_name="order_status")
    ip = models.CharField(max_length=255)
    bindingId = models.CharField(max_length=255, blank=True, null=True)
