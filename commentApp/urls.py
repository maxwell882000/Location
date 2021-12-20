from django.urls import path

from commentApp.views import specialist_comment, specialist_review, location_comment, location_review

urlpatterns = [
    path("specialist/<int:pk>/", specialist_comment),
    path("location/<int:pk>/", location_comment),
    path('specialist/review/', specialist_review),
    path('location/review/', location_review),
    path('specialist/review/<int:pk>/', specialist_review),
    path('location/review/<int:pk>/', location_review)
]
