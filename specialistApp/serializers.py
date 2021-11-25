from rest_framework import serializers
import locationApp.serializers as s
from specialistApp.models import Specialist, Category
from userApp.serializers import SerializerWithUser


class SpecialistSerializer(SerializerWithUser):
    review_avg = serializers.FloatField(default=0.0)
    location = s.LocationSerializerCard()

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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
