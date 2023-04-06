from apps.mbc.forms import MeldingAanmakenForm
from django.core.files.storage import default_storage
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


def melding_aanmaken(request):
    if request.POST:
        form = MeldingAanmakenForm(request.POST, request.FILES)
        fotos = request.FILES.getlist("fotos", [])
        file_names = []
        for f in fotos:
            file_name = default_storage.save(f.name, f)
            file_names.append(file_name)
        is_valid = form.is_valid()
        if is_valid:
            try:
                form.send_mail(fotos)
            except Exception as e:
                print(e)
            form.send_to_meldingen(file_names, request)
            return redirect("melding_verzonden")
    else:
        form = MeldingAanmakenForm()

    return render(
        request,
        "melding/aanmaken.html",
        {
            "form": form,
            "begraafplaats_medewerkers": form.get_begraafplaats_medewerkers(),
            "categorie_andere_oorzaak": form.get_categorie_andere_oorzaak(),
            "specifiek_graf_categorieen": form.get_specifiek_graf_categorieen(),
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
