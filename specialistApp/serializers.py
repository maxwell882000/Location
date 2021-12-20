from django.db import models
from django.db.models import fields
from rest_framework import serializers
import locationApp.serializers as s
from specialistApp.models import Specialist, Category
from userApp.serializers import SerializerWithUser


class SpecialistSerializer(SerializerWithUser):
    review_avg = serializers.FloatField(default=0.0)
    location = s.LocationSerializerCard()

    class Meta:
        model = Specialist
        fields = '__all__'
        depth = 2


class SpecialistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
