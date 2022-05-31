from django.urls import path

from specialistApp.views import *

urlpatterns = [
    path('list/', specialist_list),
    path('category/list/', category_list),
    path('category/list/select/', category_select_list),
    path('category/<int:pk>/', category),
    path('create/', specialist_create),
    path('update/<int:pk>/', specialist_update),

]
