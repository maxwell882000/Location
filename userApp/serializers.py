from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from userApp.models import User
import re


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
    token = serializers.CharField(max_length=255, allow_null=True, required=False)

    class Meta:
        model = User
        fields = ["id", "firstname",
                  "lastname", "token", "password",
                  "phone"]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_phone(self, phone):
        pattern = re.compile("^(\+\d*|\d*)$")
        if not pattern.match(phone):
            raise ValidationError("Incorrectly Formed")
        return phone

    def add_token(self, user):
        self.token = user.token[0].key
        self._validated_data['token'] = self.token

    def create(self, validated_data):
        phone = validated_data.pop("phone")
        password = validated_data.pop('password')
        user = User.object.create_user(phone, password, **validated_data)
        # user.send_code()
        self.add_token(user)
        return validated_data

    def update(self, instance, validated_data):
        raise Exception("Cannot be Updated")


class TokenSerializer(serializers.Serializer):
    email = serializers.CharField(
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
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
