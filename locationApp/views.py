from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from Location.mixin import WithReviewMixin
from commentApp.serializers import ReviewLocationSerializer

from locationApp.builders import location_builder
from locationApp.models import Location
from locationApp.paginator import CustomPageNumberPagination
from locationApp.serializers import *
from Location.permissions import phone_permission


class CountryLocationView(generics.ListAPIView):
    queryset = LocationCountry.objects.all().order_by("country")
    serializer_class = CountrySerializer
    pagination_class = None
    

country_list = CountryLocationView.as_view()


class CityLocationView(generics.ListAPIView):
    queryset = LocationCity.objects.all().order_by("city")
    serializer_class = CitySerializer
    pagination_class = None

    def get_queryset(self):
        return self.queryset.filter(country_id=self.request.query_params['country_id']).order_by('city')


city_list = CityLocationView.as_view()


class LocationListView(generics.ListAPIView):
    queryset = Location.objects.all().order_by("id")
    serializer_class = LocationSerializerCard
    pagination_class = CustomPageNumberPagination
    permission_classes = phone_permission

    def get_queryset(self):
        query_set = location_builder(self.request.query_params)
        return query_set.order_by("id")


location_list = LocationListView.as_view()


class LocationCreateView(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = Location.objects.all().order_by("id")
    serializer_class = LocationCreateSerializer
    permission_classes = phone_permission

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


location_create = LocationCreateView.as_view()


class ImageLocationView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = Images.objects.all().order_by("id")
    serializer_class = ImageLocationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


image_upload = ImageLocationView.as_view()

""" class LocationView(generics.GenericAPIView, WithReviewMixin):
    queryset = Location.objects.all().order_by("-id")
    serializer_class = ReviewLocationSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


location = LocationView.as_view() """
