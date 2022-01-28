from django.db import models
import json

from rest_framework import serializers


class AppLogManager:
    def create(self, request, message, view):
        user = request.user
        data = json.dumps(request.data)
        message = json.dumps(message)
        view = type(view).__name__
        log = AppLog.objects.create(request=data,
                                    message=message,
                                    view=view
                                    )
        if user.is_authenticated:
            log.user = user
            log.save()
        serializers = LogSerializer(log)
        return LogSerializer(log).data
    

class AppLog(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('userApp.User', on_delete=models.DO_NOTHING, blank=True, null=True)
    message = models.CharField(max_length=500)
    view = models.CharField(max_length=50)
    request = models.CharField(max_length=500)
    object = AppLogManager()


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppLog
        fields = '__all__'

    def to_representation(self, instance):
        """Convert `username` to lowercase."""
        ret = super().to_representation(instance)
        ret['request'] = json.loads(ret['request'])
        ret['message'] = json.loads(ret['message'])
        return ret