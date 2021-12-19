from django.urls import path

from userApp.views import obtain_token, user_view, register

urlpatterns = [
    path('api-token/', obtain_token),
    path('user/', user_view),
    path('register/', register)
]
