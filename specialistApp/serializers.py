from functools import partial
from statistics import mode
from django.db import models
from django.db.models import fields
from django.utils.functional import partition
from rest_framework import serializers
from locationApp.models import Location
import locationApp.serializers as s
from specialistApp.models import Specialist, Category
from userApp.serializers import RegisterSerializer, SerializerWithUser, UserSerilalizer
from userApp.models import User
from commonApp.models import TempImage


class SpecialistSerializer(SerializerWithUser):
    review_avg = serializers.FloatField(default=0.0)
    location = s.LocationSerializerCard()

    class Meta:
        model = Specialist
        fields = '__all__'
        depth = 2


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SpecialistCreateSerializer(serializers.ModelSerializer):
    user = RegisterSerializer()
    location = s.LocationSerializerCard()
    category = CategorySerializer()

    class Meta:
        model = Specialist
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        location = validated_data.pop("location")
        category = validated_data.pop('category')
        serialize = RegisterSerializer(data=user)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        validated_data['user'] = User.object.get(id=serialize.data['id'])
        validated_data['location'] = s.LocationSerializerCard(location)
        validated_data['category'] = CategorySerializer(category, many=True)
        return super(SpecialistCreateSerializer, self).create(validated_data)


class SpecialistUpdateSerializer(serializers.ModelSerializer):
    user = RegisterSerializer()

    class Meta:
        model = Specialist
        fields = '__all__'
        depth = 2

    def update(self, instance, validated_data):
        user = validated_data.pop('user', None)
        if user:
            serialize = RegisterSerializer(
                instance.user, data=user, partial=True)
            serialize.is_valid(raise_exception=True)
            serialize.save()
        return super().update(instance, validated_data)


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CategorySelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id',  'category_name']
