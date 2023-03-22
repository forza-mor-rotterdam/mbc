from apps.mbc.constanten import BEGRAAFPLAATS_MEDEWERKERS
from apps.mbc.forms import MeldingAanmakenForm
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
    if request.POST:
        form = MeldingAanmakenForm(request.POST, request.FILES)
        is_valid = form.is_valid()
        print(form.data)
        print(form.errors)
        if is_valid:
            form.send_mail(request.FILES.getlist("fotos", []))
            return redirect("melding_verzonden")
    else:
        form = MeldingAanmakenForm()

    return render(
        request,
        "melding/aanmaken.html",
        {
            "form": form,
            "BEGRAAFPLAATS_MEDEWERKERS": BEGRAAFPLAATS_MEDEWERKERS,
        },
    )


def melding_email(request):
    return render(
        request,
        "email/email.html",
        {
            "begraafplaats": "De Zuiderbegraafplaats",
            "grafnummer": "42",
            "vak": "F",
            "naam_overledene": "John Doe",
            "categorie": "Muizen, Andere oorzaken",
            "omschrijving_andere_oorzaken": "Andere oorzaak",
            "toelichting": "Toelichting...",
            "fotos": 0,
            "aannemer": "A.J. Verhoeven",
            "naam_melder": "Donald",
            "telefoon_melder": "0601234567",
            "email_melder": "",
            "rechthebbende": "2",
            "terugkoppeling_gewenst": "1",
        },
    )
