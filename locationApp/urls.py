from django.urls import path

from locationApp.views import *

urlpatterns = [
    path('list/', location_list),
    path('create/', location_create),
    path('city/list', city_list),
    path('country/list', country_list)
]
