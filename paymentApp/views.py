from django.shortcuts import render, redirect
from rest_framework import views

# Create your views here.
from rest_framework.response import Response

from paymentApp.models import OrderUnique
from paymentApp.service import UnBindingObject, PaymentService, ReBindingObject, RegisterObject, OrderStatusObject


class UnBindingView(views.APIView):
    def get(self, request):
        user = request.user
        deactivate = UnBindingObject(user)
        payment = PaymentService()
        return Response(payment.unBind(deactivate))


unbind_view = UnBindingView.as_view()


class ReBindingView(views.APIView):
    def get(self, request):
        user = request.user
        activate = ReBindingObject(user)
        payment = PaymentService()
        return Response(payment.reBind(activate))


rebind_view = ReBindingView.as_view()


class RegisterOrderView(views.APIView):
    def post(self, request, *args, **kwargs):
        client = request.user.user_specialist
        plan_id = request.data['plan_id']
        client.plan_id = plan_id
        client.save()
        order_unique = OrderUnique.objects.create(orderUser=client, amount=client.plan.amount)
        register = RegisterObject(order_unique, client.id)
        payment = PaymentService()
        return Response(payment.registerOrder(register))


register_object_view = RegisterOrderView.as_view()


class StatusOrderView(views.APIView):
    def get(self, request):
        user = request.user
        status = OrderStatusObject(user)
        payment = PaymentService()
        return Response(payment.statusOrder(status))


status_order_view = StatusOrderView.as_view()
