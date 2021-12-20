from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from Location.mixin import CustomCreateModelMixin, WithReviewMixin
from Location.permissions import phone_permission

from commentApp.serializers import *
from locationApp.models import Location
from specialistApp.models import Specialist


class SpecialistCommentView(generics.GenericAPIView,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            CustomCreateModelMixin):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistCommentSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, pk: int = 0, *args, **kwargs):
        self.serializer_class = CreateCommentSpecialistSerializer
        return self.create_specialist(request, pk, *args, **kwargs)

    def create_specialist(self, request, pk, *args, **kwargs):
        new_request = self.get_mutable_with_user(request)
        new_request.data['specialist'] = pk
        return self.create(new_request, *args, **kwargs)


class SpecialistReviewView(generics.GenericAPIView,
                           mixins.CreateModelMixin,
                           CustomCreateModelMixin,
                           WithReviewMixin):
    queryset = Specialist.objects.all().order_by("-id")
    serializer_class = ReviewSpecialistSerializer
    object_class = ReviewSpecialist

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.review_create(request, 'specialist', *args, **kwargs)


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

    def post(self, request, pk: int, *args, **kwargs):
        self.serializer_class = CreateCommentLocationSerializer
        return self.create_locations(request, pk, *args, **kwargs)

    def create_locations(self, request, pk, *args, **kwargs):
        new_request = self.get_mutable_with_user(request)
        new_request.data['location'] = pk
        return self.create(new_request, *args, **kwargs)


class LocationReviewView(generics.GenericAPIView,
                         mixins.CreateModelMixin,
                         CustomCreateModelMixin,
                         WithReviewMixin):
    permission_classes = phone_permission
    queryset = Location.objects.all()
    serializer_class = ReviewLocationSerializer
    object_class = ReviewLocation

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.review_create(request, 'location', *args, **kwargs)


location_comment = LocationCommentView.as_view()
location_review = LocationReviewView.as_view()
