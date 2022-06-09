from django.urls import path

from confidentialApp.views import *

urlpatterns = [
    path('get/', confidential),
    path('sales/get/', sale_text),
    path('instructions/get/', instructions)
]
