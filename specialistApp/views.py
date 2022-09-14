from django.db.models import query_utils
from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from Location.mixin import CustomCreateModelMixin, WithReviewMixin
from commentApp.serializers import ReviewSpecialistSerializer
from locationApp.paginator import CustomPageNumberPagination
from specialistApp.builders import specialist_builder
from specialistApp.models import Specialist, Category
from specialistApp.serializers import *


class SpecialistListView(generics.ListAPIView):
    queryset = Specialist.objects.all().order_by("-id")
    serializer_class = SpecialistSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        query_set = specialist_builder(self.request.query_params)
        return query_set.order_by("id")


""" class SpecialistView(generics.GenericAPIView, WithReviewMixin):
    queryset = Specialist.objects.all().order_by("-id")
    serializer_class = ReviewSpecialistSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
 """

specialist_list = SpecialistListView.as_view()
""" specialist = SpecialistView.as_view()
 """


# temp for avatar
class SpecialistCreateView(generics.GenericAPIView,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           CustomCreateModelMixin):
    queryset = Specialist.objects.all().order_by('-id')
    permission_classes = [AllowAny]
    serializer_class = SpecialistCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create_temp(request, 'image', *args, **kwargs)


class SpecialistUpdateView(generics.GenericAPIView,
                           CustomCreateModelMixin,
                           mixins.UpdateModelMixin, ):
    queryset = Specialist.objects.all().order_by('-id')
    permission_classes = [AllowAny]
    serializer_class = SpecialistUpdateSerializer

    def put(self, request, *args, **kwargs):
        return self.update_temp(request, 'image', *args, **kwargs)


specialist_create = SpecialistCreateView.as_view()

specialist_update = SpecialistUpdateView.as_view()


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().filter(is_active=True).order_by('-id')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class CategorySelectListView(CategoryListView):
    pagination_class = CustomPageNumberPagination


class CategoryView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


category_list = CategoryListView.as_view()
category = CategoryView.as_view()
category_select_list = CategorySelectListView.as_view()
