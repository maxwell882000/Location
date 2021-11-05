from django.contrib import admin


class ActiveFilter(admin.SimpleListFilter):
    title = "Активированные Локации"
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (
            (True, "Активированые"),
            (False, "Не активированые"),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(is_active=self.value())
        return queryset
