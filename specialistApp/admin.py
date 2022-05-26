from django.contrib import admin
from django.contrib.admin import ModelAdmin

from specialistApp.filter import ActiveSpecialistFilter
from specialistApp.models import Specialist, Category


class SpecialistAdmin(ModelAdmin):
    filter_horizontal = ["category"]
    list_filter = [
        ActiveSpecialistFilter
    ]


admin.site.register(Specialist, SpecialistAdmin)
admin.site.register(Category)
