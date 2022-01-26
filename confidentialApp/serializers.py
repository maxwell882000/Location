from django.forms import fields
from rest_framework import serializers
from .models import Confidential


class ConfidentialSerializers(serializers.ModelSerializer):
    class Meta:
        model = Confidential
        fields = "__all__"
