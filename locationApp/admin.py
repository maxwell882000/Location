from django.contrib.admin import AdminSite
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django_admin_geomap import ModelAdmin

from Location import settings
from locationApp.filter import ActiveFilter
from locationApp.models import Location, Images, LocationCity, LocationCountry

AdminSite.site_title = "Админка"
AdminSite.site_header = "Локация"
AdminSite.index_title = "Админка"
admin.site.unregister(Group)


class LocationAdmin(ModelAdmin):
    geomap_field_longitude = "id_longitude"
    geomap_field_latitude = "id_latitude"
    actions = ("see_inactive",)
    list_filter = (ActiveFilter,)
    filter_horizontal = ["images"]


admin.site.register(LocationCountry)
admin.site.register(LocationCity)
admin.site.register(Location, LocationAdmin)
admin.site.register(Images)
