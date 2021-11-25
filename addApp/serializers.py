from rest_framework import serializers

from addApp.models import Add


class AddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add
        fields = "__all__"