from rest_framework import serializers

from commonApp.models import CommonLogo, CommonIcon, TempImage


class CommonLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonLogo
        fields = '__all__'

class TempSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempImage
        fields = "__all__"

class CommonIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonIcon
        fields = '__all__'
