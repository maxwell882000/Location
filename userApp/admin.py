from django.contrib import admin
from django.contrib.admin import ModelAdmin

from specialistApp.models import Specialist
from userApp.models import User


class UserAdmin(ModelAdmin):
    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        return qs.exclude(pk__in=Specialist.objects.values_list('user_id', flat=True))


admin.site.register(User, UserAdmin)
