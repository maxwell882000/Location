from import_export import resources, fields
from locationApp.models import LocationCity, LocationCountry

from import_export.widgets import ForeignKeyWidget


class CountryField(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        val = super(ForeignKeyWidget, self).clean(value)
        if val:
            return self.get_queryset(value, row, *args, **kwargs).get_or_create(**{self.field: val})[0]
        else:
            return None


class CityResource(resources.ModelResource):
    country = fields.Field(attribute="country",
                           widget=CountryField(LocationCountry, "country"),
                           column_name="country")

    class Meta:
        model = LocationCity
