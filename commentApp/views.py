from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import AllowAny

from commentApp.serializers import *
from locationApp.models import Location
from specialistApp.models import Specialist


class SpecialistCommentView(generics.GenericAPIView,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistCommentSerializer
    pagination_class = None
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = CreateCommentSpecialistSerializer
        return self.create(request, *args, **kwargs)


class SpecialistReviewView(generics.GenericAPIView,
                           mixins.CreateModelMixin):
    serializer_class = ReviewSpecialistSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


specialist_comment = SpecialistCommentView.as_view()
specialist_review = SpecialistReviewView.as_view()


class LocationCommentView(generics.GenericAPIView,
                          mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin):
    queryset = Location.objects.all()
    serializer_class = LocationCommentSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = CreateCommentLocationSerializer
        return self.create(request, *args, **kwargs)


class LocationReviewView(generics.GenericAPIView,
                         mixins.CreateModelMixin):
    serializer_class = ReviewLocationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


location_comment = LocationCommentView.as_view()
location_review = LocationReviewView.as_view()
