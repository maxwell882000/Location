from django.contrib import admin


class ActiveSpecialistFilter(admin.SimpleListFilter):
    parameter_name = 'is_deactivated'

    def lookups(self, request, model_admin):
        return (
            (True, "Активированые"),
            (False, "Не активированые"),
        )
