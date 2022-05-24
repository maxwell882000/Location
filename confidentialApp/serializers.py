from django.forms import fields
from rest_framework import serializers
from .models import Confidential, SaleText


class ConfidentialSerializers(serializers.ModelSerializer):
    class Meta:
        model = Confidential
        fields = "__all__"

class SaleTextSerializers(serializers.ModelSerializer):
    class Meta:
        model = SaleText
        fields = "__all__"