from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny

from locationApp.builders import location_builder
from locationApp.models import Location
from locationApp.paginator import CustomPageNumberPagination
from locationApp.serializers import *

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
# class LocationCardSearch(generics.ListAPIView):
#     serializer_class = LocationSerializerCard
#     model = serializer_class.Meta.model
#     permission_classes = [AllowAny]
#     paginate_by = 10


# location_search = LocationCardSearch().as_view()
