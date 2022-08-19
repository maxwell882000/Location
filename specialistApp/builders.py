from specialistApp.models import Specialist


def specialist_builder(filter_by: dict):
    specialist = Specialist.objects
    if 'location' in filter_by:
        specialist = specialist.filter(location_id=filter_by['location'])
    return specialist.filter(days_activated__gt=-1)
