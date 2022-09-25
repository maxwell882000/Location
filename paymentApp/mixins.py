from paymentApp.models import OrderUnique
from paymentApp.service import RegisterObject, PaymentService, OrderStatusObject, BindPaymentObject, GetBindingInfo


class RegisterOrder:

    def prepare_register_params(self, specialist, order_unique):
        register_params = {
            'amount': order_unique.amount * 100,
            'route': "/success_payment",
            'order_unique': order_unique,
            'client': specialist,
        }
        if hasattr(specialist, 'order_status'):
            print("")
            if specialist.order_status.bindingId == None:
                get_bind = GetBindingInfo(specialist)
                PaymentService().getBind(get_bind)
            register_params['bindingId'] = specialist.order_status.bindingId
            register_params['features'] = "AUTO_PAYMENT"
        else:
            register_params['route'] = "/waiting_payment"
            register_params['features'] = "VERIFY"
            register_params['amount'] = 0

        return register_params

    def order_register(self, specialist):
        order_unique = OrderUnique.objects.create(order_user=specialist, amount=specialist.plan.amount)
        register = RegisterObject(self.prepare_register_params(specialist, order_unique))
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
