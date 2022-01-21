from functools import partial
from pkgutil import read_code
from statistics import mode
from django.db import models
from django.db.models import fields
from django.utils.functional import partition
from rest_framework import serializers
from Location.settings import SITE
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

    class Meta:
        model = Specialist
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        serialize = RegisterSerializer(data=user)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        validated_data['user'] = User.object.get(id=serialize.data['id'])
        return super(SpecialistCreateSerializer, self).create(validated_data)

    def to_representation(self, instance):
        render = super().to_representation(instance)
        render['location'] = s.LocationSerializerCard(
            Location.objects.get(id=render['location'])).data
        render['category'] = CategorySerializer(
            Category.objects.filter(id__in=render['category']), many=True).data
        return render
    def get_image(self, specialist):
        return "{}{}".format(SITE, specialist.image.url)


class SpecialistUpdateSerializer(serializers.ModelSerializer):
    user = serializers.DictField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Specialist
        fields = '__all__'
        depth = 2

    def update(self, instance, validated_data):
        user = validated_data.pop('user', None)
        if user:
            serializer = RegisterSerializer(instance=instance.user, data=user, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # if validated_data['phone'] == instance.phone:
            #     instance.user.phone = validated_data.pop('phone')
            # instance.user.firstname = validated_data.pop('firstname')
            # instance.user.lastname = validated_data.pop('lastname')
            # instance.user.save()
        return super().update(instance, validated_data)

    def get_image(self, specialist):
        return "{}{}".format(SITE, specialist.image.url)


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CategorySelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id',  'category_name']
