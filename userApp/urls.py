from django.urls import path

from userApp.views import obtain_token, user_view

urlpatterns = [
    path('api-token/', obtain_token),
    path('register/', user_view)
]
