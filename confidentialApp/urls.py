from django.urls import path

from confidentialApp.views import *

urlpatterns = [
    path('get/', confidential),
]
