from rest_framework import serializers

from locationApp.models import Images, Location, LocationCity, LocationCountry
from specialistApp.models import Category


class LocationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class CategoryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCity
        fields = "__all__"
        depth = 0


class CitySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCity
        fields = "__all__"
        depth = 1


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCountry
        fields = "__all__"
        depth = 0


class ImageLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
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
