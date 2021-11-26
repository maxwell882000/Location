from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework import mixins
from specialistApp.builders import specialist_builder
from specialistApp.models import Specialist, Category
from specialistApp.serializers import *


class SpecialistListView(generics.ListAPIView):
    queryset = Specialist.objects.all().order_by("-id")
    serializer_class = SpecialistSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        print(self.request.query_params)
        query_set = specialist_builder(self.request.query_params)
        return query_set.order_by("id")


class SpecialistView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = Specialist.objects.all().order_by("-id")
    serializer_class = SpecialistSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


specialist_list = SpecialistListView.as_view()
specialist = SpecialistView.as_view()


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class CategoryView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


category_list = CategoryListView.as_view()
category = CategoryView.as_view()
