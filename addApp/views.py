from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import AllowAny

from addApp.models import Add
from addApp.serializers import AddSerializer


class AddListView(generics.ListAPIView):
    queryset = Add.objects.all().order_by("-id")
    serializer_class = AddSerializer
    permission_classes = [AllowAny]
    pagination_class = None


add_list = AddListView.as_view()
