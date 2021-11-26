from rest_framework import serializers

from locationApp.models import Location
from specialistApp.models import Category


class LocationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class CategoryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class LocationSerializerCard(serializers.ModelSerializer):
    city = serializers.CharField(source="city_str")
    review_avg = serializers.FloatField(default=0.0)
    country = serializers.CharField(source="country_str")
    category = CategoryLocationSerializer(many=True)

    class Meta:
        model = Location
        fields = '__all__'
        depth = 1
