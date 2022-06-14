from django.urls import path

from locationApp.views import *
from planApp.views import plan_view

urlpatterns = [
    path('get/', plan_view),
]
