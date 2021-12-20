from django.urls import path

from locationApp.views import *

urlpatterns = [
    path('list/', location_list),
    path('create/', location_create),
    path('<int:pk>', location)
    # path('list/search/', location_search)
]
