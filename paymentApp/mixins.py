from paymentApp.models import OrderUnique
from paymentApp.service import RegisterObject, PaymentService, OrderStatusObject, BindPaymentObject


class RegisterOrder:
    def order_register(self, specialist):
        order_unique = OrderUnique.objects.create(order_user=specialist, amount=specialist.plan.amount)
        register = RegisterObject(order_unique, specialist.id)
        payment = PaymentService()
        return payment.registerOrder(register)

    def auto_payment(self, specialist):
        binding = BindPaymentObject(specialist)
        payment = PaymentService()
        return payment.bindingPayment(binding)


class StatusOrder:
    def status_order(self, specialist):
        status = OrderStatusObject(specialist)
        payment = PaymentService()
        return payment.statusOrder(status)
