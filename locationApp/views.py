from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny
from Location.mixin import WithReviewMixin
from commentApp.serializers import ReviewLocationSerializer

from locationApp.builders import location_builder
from locationApp.models import Location
from locationApp.paginator import CustomPageNumberPagination
from locationApp.serializers import *


class CountryLocationView(generics.ListAPIView):
    queryset = LocationCountry.objects.all().order_by("country")
    serializer_class = CountrySerializer
    pagination_class = CustomPageNumberPagination


country_list = CountryLocationView.as_view()


class CityLocationView(generics.ListAPIView):
    queryset = LocationCity.objects.all().order_by("city")
    serializer_class = CitySerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return self.queryset.filter(country_id=self.request.data['country_id']).order_by('city')


city_list = CityLocationView.as_view()


class LocationListView(generics.ListAPIView):
    queryset = Location.objects.all().order_by("id")
    serializer_class = LocationSerializerCard
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        query_set = location_builder(self.request.query_params)
        return query_set.order_by("id")


location_list = LocationListView.as_view()


class LocationCreateView(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = Location.objects.all().order_by("id")
    serializer_class = LocationCreateSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


location_create = LocationCreateView.as_view()

""" class LocationView(generics.GenericAPIView, WithReviewMixin):
    queryset = Location.objects.all().order_by("-id")
    serializer_class = ReviewLocationSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


location = LocationView.as_view() """
