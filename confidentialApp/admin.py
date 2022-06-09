from django.contrib import admin

from confidentialApp.models import Confidential, SaleText, Instructions

admin.site.register(Confidential)
admin.site.register(SaleText)
admin.site.register(Instructions)
