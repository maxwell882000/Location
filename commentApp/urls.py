from django.urls import path

from commentApp.views import specialist_comment, specialist_review

urlpatterns = [
    path("specialist/<int:pk>/", specialist_comment),
    path("specialist/list/", specialist_comment),
    path('specialist/review/', specialist_review),
    path("location/<int:pk>/", specialist_comment),
    path("location/list/", specialist_comment),
    path('location/review/', specialist_review)
]
