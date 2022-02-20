from django.urls import path

from locationApp.views import *

urlpatterns = [
    path('list/', location_list),
    path('create/', location_create),
    path('city/list', city_list),
    path('image/upload', image_upload),
    path('image/delete/<int:pk>', image_upload),
    path('country/list', country_list),
    path("city/list/search", city_search_list)
]
