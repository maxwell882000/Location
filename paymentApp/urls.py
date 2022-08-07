from django.urls import path

from paymentApp.views import unbind_view, rebind_view, register_object_view, status_order_view

urlpatterns = [
    path('unbind/', unbind_view),
    path("rebind/", rebind_view),
    path("register_order/", register_object_view),
    path("status_order/", status_order_view)
]
