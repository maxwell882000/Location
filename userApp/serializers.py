from pyexpat import model
from unicodedata import category
from django.conf import settings
from django.contrib.auth import authenticate
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
import locationApp.serializers as s
from specialistApp.models import Category, Specialist
from Location.settings import SITE
from userApp.models import User
import re


class NewPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.set_password(password)
        instance.is_phone_reset_validate = False
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CustomImageField(serializers.ImageField):
    def to_representation(self, value):
        return "{}{}".format(SITE, value.url)


class SpecialistSerializer(serializers.ModelSerializer):
    review_avg = serializers.FloatField(default=0.0)
    location = s.LocationSerializerCard()
    category = CategorySerializer(many=True)
    image = CustomImageField()
    is_deactivated = serializers.BooleanField(default=True)
    is_auto_payment = serializers.BooleanField(default=False)

    class Meta:
        model = Specialist
        exclude = ('user',)


class UserSerilalizer(serializers.ModelSerializer):
    user_specialist = SpecialistSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'firstname',
            'lastname',
            'user_specialist',
            'phone'
        )


class UserSpecialistCard(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'firstname',
            'lastname',
            'phone'
        )


class SerializerWithUser(serializers.ModelSerializer):
    user = UserSpecialistCard()


class RegisterSerializer(serializers.ModelSerializer):
    token = serializers.CharField(
        max_length=700, allow_null=True, required=False)

    class Meta:
        model = User
        fields = [
            "id", "firstname", "phone",
            "lastname", "token", "password",
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def add_token(self, user, validated_data):
        self.token = user.token
        validated_data['token'] = self.token

    def create(self, validated_data):
        phone = validated_data.pop("phone")
        password = validated_data.pop('password')
        user = User.object.create_user(phone, password, **validated_data)
        self.add_token(user, validated_data)
        validated_data['phone'] = phone
        validated_data['id'] = user.id
        return validated_data

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        instance.firstname = validated_data.pop('firstname')
        instance.phone = validated_data.pop('phone')
        instance.lastname = validated_data.pop('lastname')
        instance.save()
        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "firstname",
                  "lastname", "password",
                  "phone"]

    # def get_validation_exclusions(self):
    #     exclusions = super(UpdateUserSerializer,
    #                        self).get_validation_exclusions()
    #     return exclusions + self.Meta.fields

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        return super(UpdateUserSerializer, self).update(instance, validated_data)


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class TokenSerializer(serializers.Serializer):
    phone = serializers.CharField(
        label=_("Phone"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")

        if phone and password:
            user = authenticate(request=self.context.get('request'),
                                username=phone, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = 'Не правильный ввод данных'
                raise serializers.ValidationError(
                    {"errors": msg}, code='authorization')
        else:
            msg = 'Должны ввести пароль и телефонный номер'
            raise serializers.ValidationError(
                {"errors": msg}, code='authorization')

        attrs['user'] = user
        return attrs
