from celery import shared_task

from paymentApp.mixins import RegisterOrder
from specialistApp.models import Specialist


class AutoPayment(RegisterOrder):
    def __init__(self):
        self.specialists = Specialist.objects.filter(days_activated=0,
                                                     order_status__bindingId__isnull=False).get()

    def run(self):
        for specialist in self.specialists.all():
            self.order_register(specialist)
            self.auto_payment(specialist)


@shared_task(name="auto_bind")
def auto_bind():
    payment = AutoPayment()
    payment.run()


@shared_task(name="minus_days")
def minus_days():
    specialists = Specialist.objects.filter(days_activated__gt=0).get()
    specialists.days_activated -= 1
    specialists.save()
