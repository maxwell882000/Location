from django.db.models.signals import post_delete
# I have used django user model to use post save, post delete.
from django.dispatch import receiver

from specialistApp.models import Specialist


@receiver(post_delete, sender=Specialist)
def delete_user(sender, instance, *args, **kwargs):
    instance.user.delete()
