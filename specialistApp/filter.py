from django.contrib import admin


class ActiveSpecialistFilter(admin.SimpleListFilter):
    parameter_name = 'days_activated'
    title = "Активированные Специалисты"

    def lookups(self, request, model_admin):
        return (
            (True, "Активированые"),
            (False, "Не активированые"),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            if self.value() == 'True':
                return queryset.filter(days_activated__gt=0)
            else:
                return queryset.filter(days_activated=0)
        return queryset
