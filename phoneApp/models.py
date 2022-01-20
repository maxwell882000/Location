import random

from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from userApp.models import User


class PhoneVerifier(models.Model):
    code = models.IntegerField(default=0)
    user = models.OneToOneField("userApp.User", on_delete=models.CASCADE, related_name="phone_validation")

    def save(self, *args, **kwargs):
        self.code = random.randint(1000, 9999)
        return super(PhoneVerifier, self).save(*args, **kwargs)

    def validate(self, code):
        if self.code == int(code):
            self.user.is_phone_validated = True
            self.user.save()
            return True
        return False


@receiver(post_save, sender=User)
def createPhoneVerifier(sender, instance, created, *args, **kwargs):
    if created:
        PhoneVerifier.objects.create(user=instance)
