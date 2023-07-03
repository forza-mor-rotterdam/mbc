from apps.main.models import Begraafplaats, Categorie, Medewerker
from django.contrib import admin
from django.contrib.admin import AdminSite

AdminSite.site_title = "Begraven & cremeren - Serviceformulierbeheer"
AdminSite.site_header = "Begraven & cremeren - Serviceformulierbeheer"
AdminSite.index_title = "Serviceformulierbeheer"


class BegraafplaatsAdmin(admin.ModelAdmin):
    list_display = ("naam", "begraafplaats_medewerkers")

    def begraafplaats_medewerkers(self, obj):
        return ", ".join(list(obj.medewerkers.all().values_list("naam", flat=True)))


class MedewerkerAdmin(admin.ModelAdmin):
    list_display = ("naam", "actief_op_begraafplaats")
    filter_horizontal = ("begraafplaatsen",)

    def actief_op_begraafplaats(self, obj):
        return ", ".join(list(obj.begraafplaatsen.all().values_list("naam", flat=True)))


class CategorieAdmin(admin.ModelAdmin):
    list_display = (
        "naam",
        "volgorde",
        "toon_andere_oorzaak",
        "toon_specifiek_graf",
    )
    list_editable = (
        "volgorde",
        "toon_andere_oorzaak",
        "toon_specifiek_graf",
    )


admin.site.register(Begraafplaats, BegraafplaatsAdmin)
admin.site.register(Medewerker, MedewerkerAdmin)
admin.site.register(Categorie, CategorieAdmin)
