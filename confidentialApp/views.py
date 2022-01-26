from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins

from confidentialApp.models import Confidential
from confidentialApp.serializers import ConfidentialSerializers


class ConfidentialView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = Confidential.objects.all().order_by('-id')
    serializer_class = ConfidentialSerializers

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        return Confidential.objects.last()

confidential = ConfidentialView.as_view()