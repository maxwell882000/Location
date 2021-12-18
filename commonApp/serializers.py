from rest_framework import serializers

from commonApp.models import CommonLogo, CommonIcon


class CommonLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonLogo
        fields = '__all__'


class CommonIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonIcon
        fields = '__all__'
