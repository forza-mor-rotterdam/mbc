from apps.services.mail import MailService
from apps.signalen.models import Signaal
from django.contrib import admin


@admin.action(description="Verstuur 'melding afgesloten' email")
def action_verstuur_melding_afgesloten_email(modeladmin, request, queryset):
    for signaal in queryset.all():
        MailService().melding_afgesloten_mail(
            signaal=signaal,
        )


class SignaalAdmin(admin.ModelAdmin):
    list_display = ("id", "uuid", "afgesloten_op")
    actions = (action_verstuur_melding_afgesloten_email,)


admin.site.register(Signaal, SignaalAdmin)
