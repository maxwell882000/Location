from django.urls import path

from specialistApp.views import *

urlpatterns = [
    path('list/', specialist_list),
    path('<int:pk>/', specialist),
    path('category/list/', category_list),
    path('category/<int:pk>/', category)
]
