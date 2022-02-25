from django.db.models import Q, F, FloatField, ExpressionWrapper

from locationApp.models import Location


def location_builder(filter_by: dict):
    builder = Q()
    location = Location.objects
    if 'latitude' in filter_by and 'longitude' in filter_by and 'radius' in filter_by:
        lat = float(filter_by['latitude'])
        long = float(filter_by['longitude'])
        rad = int(filter_by['radius'])
        location = location.annotate(radius_sqr=ExpressionWrapper(pow(F("latitude") -
                                                                      lat, 2) + pow(F('longitude') - long, 2),
                                                                  output_field=FloatField()))
        builder = builder & Q(radius_sqr__lte=pow(rad / 9, 2))
    if 'search' in filter_by:
        search = filter_by['search']
        builder = builder & Q(district__icontains=search)
    if 'locations' in filter_by:
        builder = builder & ~Q(pk__in=filter_by.getlist('locations'))
    if 'category' in filter_by:
        id = int(filter_by['category'])
        builder = builder & (Q(specialist__category=id) | Q(category_location = id) )
    
    return location.filter(is_active=True).filter(builder & ~Q(city=None)).distinct()
