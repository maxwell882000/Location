from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins

from confidentialApp.models import Confidential, SaleText, Instructions
from confidentialApp.serializers import ConfidentialSerializers, SaleTextSerializers


class ConfidentialView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = Confidential.objects.all().order_by('-id')
    serializer_class = ConfidentialSerializers

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        return Confidential.objects.last()


confidential = ConfidentialView.as_view()


class SaleTextView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = SaleText.objects.all().order_by("-id")
    serializer_class = SaleTextSerializers

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        return SaleText.objects.last()


sale_text = SaleTextView.as_view()


class SaleTextView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = Instructions.objects.all().order_by("-id")
    serializer_class = SaleTextSerializers

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        return Instructions.objects.last()


instructions = SaleTextView.as_view()
