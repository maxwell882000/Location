from django.contrib import admin


class ActiveSpecialistFilter(admin.SimpleListFilter):
    parameter_name = 'is_deactivated'
    title = "Активированные Специалисты"

    def lookups(self, request, model_admin):
        return (
            (True, "Активированые"),
            (False, "Не активированые"),
        )
