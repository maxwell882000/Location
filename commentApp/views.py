from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import AllowAny

from commentApp.serializers import *
from locationApp.models import Location
from specialistApp.models import Specialist

from django.http import QueryDict


class RequestCustom:
    data = {}

    def __init__(self, data: dict) -> None:
        self.data = QueryDict.copy(data)


class CustomCreateModelMixin:
    object_class = None

    def get_mutable_with_user(self, request):
        new_request = RequestCustom(request.data)
        new_request.data['user'] = request.user.id
        return new_request

    def create_custom(self, request, *args, **kwargs):
        new_request = self.get_mutable_with_user(request)
        return self.create(new_request, *args, **kwargs)

    def review_create(self, request, field_name, *args, **kwargs):
        new_request = self.get_mutable_with_user(request)
        object = self.object_class.objects.filter(
            user=request.user,
            specialist=new_request.data[field_name]
        )
        if object.exists():
            new_request.data['id'] = object.id
        return self.create_custom(request, *args, **kwargs)


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
                           CustomCreateModelMixin):

    serializer_class = ReviewSpecialistSerializer
    permission_classes = [AllowAny]
    object_class = ReviewSpecialist

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
                         CustomCreateModelMixin):
    serializer_class = ReviewLocationSerializer
    object_class = ReviewLocation

    def post(self, request, *args, **kwargs):
        return self.review_create(request, 'location', *args, **kwargs)


location_comment = LocationCommentView.as_view()
location_review = LocationReviewView.as_view()
