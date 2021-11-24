from rest_framework import serializers

from locationApp.models import Location
from specialistApp.models import Specialist
from userApp.models import User


class UserSpecialistCard(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'firstname',
            'lastname',
            'phone'
        )


class SpecialistSerializerCard(serializers.ModelSerializer):
    review_avg = serializers.FloatField(default=0.0)
    user = UserSpecialistCard()

    class Meta:
        model = Specialist
        fields = ("id",
                  "image",
                  "review_avg",
                  'category',
                  "location",
                  'user'
                  )
        depth = 2


class SpecialistSerializer(serializers.ModelSerializer):
    pass
