from django.urls import path

from userApp.views import obtain_token, user_view, register, verify_code, update, password_change, check_view, \
    forget_password

urlpatterns = [
    path('api-token/', obtain_token),
    path('user/', user_view),
    path('check/', check_view),
    path('user/code/', verify_code),
    path('user/code/<str:phone>/', verify_code),
    path('register/', register),
    path('update/', update),
    path('change_password/', password_change),
    path('forget_password/<str:phone>/', forget_password)
]
