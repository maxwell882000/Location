from django.urls import path

from specialistApp.views import card_specialist

urlpatterns = [
    path('card/', card_specialist),
]
