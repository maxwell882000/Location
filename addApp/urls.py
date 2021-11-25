from django.urls import path

from addApp.views import add_list

urlpatterns = [
    path("list/", add_list),
]
