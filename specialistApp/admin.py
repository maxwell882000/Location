from django.contrib import admin
from django.contrib.admin import ModelAdmin

from specialistApp.filter import ActiveSpecialistFilter
from specialistApp.models import Specialist, Category


@admin.action(description='Деактивировать виды деятельности')
def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description='Активировать виды деятельности')
def acivate(modeladmin, request, queryset):
    queryset.update(is_active=True)


class CategoryAdmin(ModelAdmin):
    actions = [deactivate, acivate]


class SpecialistAdmin(ModelAdmin):
    filter_horizontal = ["category"]
    list_filter = [
        ActiveSpecialistFilter
    ]


admin.site.register(Specialist, SpecialistAdmin)
admin.site.register(Category,CategoryAdmin)
