from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import AllowAny

from commentApp.serializers import *
from locationApp.models import Location
from specialistApp.models import Specialist


class RequestCustom:
    data = {}

    def __init__(self, data: dict) -> None:
        self.data = data


class CustomCreateModelMixin:
    def create_custom(self, request, *args, **kwargs):
        new_request = RequestCustom(request.data)
        new_request.data['user'] = request.user.id
        return self.create(new_request, *args, **kwargs)


class SpecialistCommentView(generics.GenericAPIView,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            CustomCreateModelMixin):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistCommentSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, pk=0, *args, **kwargs):
        self.serializer_class = CreateCommentSpecialistSerializer
        return self.create_custom(request, *args, **kwargs)


class SpecialistReviewView(generics.GenericAPIView,
                           mixins.CreateModelMixin,
                           CustomCreateModelMixin):
    serializer_class = ReviewSpecialistSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return self.create_custom(request, *args, **kwargs)


specialist_comment = SpecialistCommentView.as_view()
specialist_review = SpecialistReviewView.as_view()


class LocationCommentView(generics.GenericAPIView,
                          mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin,
                          CustomCreateModelMixin):
    queryset = Location.objects.all()
    serializer_class = LocationCommentSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = CreateCommentLocationSerializer
        return self.create_custom(request, *args, **kwargs)


class LocationReviewView(generics.GenericAPIView,
                         mixins.CreateModelMixin,
                         CustomCreateModelMixin):
    serializer_class = ReviewLocationSerializer

    def post(self, request, *args, **kwargs):
        return self.create_custom(request, *args, **kwargs)


location_comment = LocationCommentView.as_view()
location_review = LocationReviewView.as_view()
