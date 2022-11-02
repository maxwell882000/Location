from specialistApp.models import Specialist


def specialist_builder(filter_by: dict):
    specialist = Specialist.objects
    if 'location' in filter_by:
        specialist = specialist.filter(many_location__in=[filter_by['location']]).distinct()
    return specialist.filter(days_activated__gt=-1)


def reRunLocations():
    specialists = Specialist.objects.all()
    for specialist in specialists:
        if specialist.location != None:
            specialist.many_location.add(specialist.location.id)
            specialist.save()
