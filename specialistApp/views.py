from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from specialistApp.models import Specialist
from specialistApp.serializers import SpecialistSerializerCard


class SpecialistCardView(generics.ListAPIView):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializerCard
    permission_classes =  [AllowAny]


card_specialist = SpecialistCardView.as_view()
