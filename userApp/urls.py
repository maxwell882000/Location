from django.urls import path

from userApp.views import obtain_token, user_view, register, verify_code, update, password_change, check_view

urlpatterns = [
    path('api-token/', obtain_token),
    path('user/', user_view),
    path('check/', check_view),
    path('user/code/', verify_code),
    path('register/', register),
    path('update/', update),
    path('change_password/', password_change)
]
