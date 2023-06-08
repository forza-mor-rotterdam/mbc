from apps.signalen.models import Signaal
from django.contrib import admin


class SignaalAdmin(admin.ModelAdmin):
    list_display = ("id", "uuid", "afgesloten_op")


admin.site.register(Signaal, SignaalAdmin)
