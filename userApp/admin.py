from django.contrib import admin
from django.contrib.admin import ModelAdmin

from specialistApp.models import Specialist
from userApp.models import User


class UserAdmin(ModelAdmin):
    def get_queryset(self, request):
        return User.object.exclude(pk__in=Specialist.objects.values_list('user_id', flat=True)).order_by('-id')


admin.site.register(User)
