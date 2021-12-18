from django.urls import path

from commonApp.views import common

urlpatterns = [
    path("app/", common),
]
