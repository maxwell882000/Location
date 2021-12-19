from rest_framework import serializers

from commentApp.models import CommentSpecialist, ReviewSpecialist, CommentLocation, ReviewLocation
from locationApp.models import Location
from specialistApp.models import Specialist
from userApp.serializers import SerializerWithUser


class CommentSpecialistSerializer(SerializerWithUser):
    class Meta:
        model = CommentSpecialist
        fields = ('comment', 'user', 'date')
        depth = 0


class CommentLocationSerializer(SerializerWithUser):
    class Meta:
        model = CommentLocation
        fields = ('comment', 'user','date')
        depth = 0


class CreateCommentSpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentSpecialist
        fields = '__all__'
        depth = 1


class ReviewSpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewSpecialist
        fields = '__all__'
        depth = 1


class ReviewLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLocation
        fields = '__all__'
        depth = 1


class SpecialistCommentSerializer(serializers.ModelSerializer):
    comments = CommentSpecialistSerializer(many=True)

    class Meta:
        model = Specialist
        fields = (
            'comments',
        )


class CreateCommentLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLocation
        fields = '__all__'
        depth = 1


class LocationCommentSerializer(serializers.ModelSerializer):
    comments = CommentLocationSerializer(many=True)

    class Meta:
        model = Location
        fields = (
            'comments',
        )
