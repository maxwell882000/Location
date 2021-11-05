from django.urls import path

from userApp.views import obtain_token, register

urlpatterns = [
    path('api-token/', obtain_token),
    path('register/', register)
]
