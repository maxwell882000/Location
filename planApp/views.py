from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from planApp.models import Plan
from planApp.serializers import PlanSerializer


class PlanListView(generics.ListAPIView):
    queryset = Plan.objects.all().order_by("id")
    serializer_class = PlanSerializer
    pagination_class = None
    permission_classes = [AllowAny]


plan_view = PlanListView.as_view()
