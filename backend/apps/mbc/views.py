import json

from apps.mbc.constanten import BEGRAAFPLAATS_EMAIL_ADRES
from apps.mbc.forms import MeldingAanmakenForm
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse


def http_404(request):
    return render(
        request,
        "404.html",
    )


def http_500(request):
    return render(
        request,
        "500.html",
    )


def root(request):
    return redirect(reverse("melding_aanmaken"))


def handle_uploaded_file(f):
    with open("/media/name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def melding_aanmaken(request):
    dirty_fields_list = []
    if request.POST:
        form = MeldingAanmakenForm(request.POST, request.FILES)
        is_valid = form.is_valid()
        print(request.FILES)
        print(form.data)
        print(form.errors)
        dirty_fields_list = json.loads(form.data.get("dirty_fields", "[]"))
        if is_valid:
            send_to = []
            if BEGRAAFPLAATS_EMAIL_ADRES.get(form.cleaned_data.get("begraafplaats")):
                send_to.append(
                    BEGRAAFPLAATS_EMAIL_ADRES.get(
                        form.cleaned_data.get("begraafplaats")
                    )
                )
            if form.cleaned_data.get("email_melder"):
                send_to.append(form.cleaned_data.get("email_melder"))
            send_mail(
                "Begraven & cremeren Service aanvraag",
                "Dit is een standaard tekst voor B&C",
                settings.DEFAULT_FROM_EMAIL,
                send_to,
                fail_silently=False,
            )
            return redirect("melding_verzonden")
    else:
        form = MeldingAanmakenForm()

    return render(
        request,
        "melding/aanmaken.html",
        {
            "form": form,
            "dirty_fields_list": dirty_fields_list,
        },
    )


def melding_email(request):
    return render(
        request,
        "email/email.html",
        {
            "formdata": {
                "begraafplaats": "Zuiderbegraafplaats",
                "Grafnummer": "18",
                "Vak": "C",
                "Naam overledene": "A. Jansen",
                "categorie": ", ".join(["Snoeien"]),
                "Andere oorzaken": "",
                "Toelichting": "Graag de overhangende takken verwijderen.",
                "Medewerker": "A. van de Graaf",
                "Naam melder": "D. Melder",
                "Telefoonnummer melder": "06-12345678",
                "E-mailadres": "",
                "Rechthebbende": "Ja",
                "Terugkoppeling gewenst?": "Ja",
            }
        },
    )
