from django.urls import path

from commonApp.views import *

urlpatterns = [
    path("app/", common),
    path("temp_store/", temp_view)
]
