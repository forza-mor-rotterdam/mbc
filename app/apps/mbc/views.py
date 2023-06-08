import logging

from apps.mbc.forms import MeldingAanmakenForm
from apps.services.mail import MailService
from apps.services.meldingen import MeldingenService
from apps.signalen.models import Signaal
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

logger = logging.getLogger(__name__)


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
            signaal = Signaal.acties.signaal_aanmaken(
                form.signaal_data(file_names), request=request
            )
            form.send_mail(file_names)
            return redirect(
                reverse("melding_verzonden", kwargs={"signaal_uuid": signaal.uuid})
            )
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


def melding_verzonden(request, signaal_uuid):
    signaal = get_object_or_404(Signaal, uuid=signaal_uuid)
    meldingen_signaal_response = MeldingenService().signaal_ophalen(
        signaal.meldingen_signaal_url
    )
    meldingen_signaal = {}
    if meldingen_signaal_response.status_code == 200:
        meldingen_signaal = meldingen_signaal_response.json()
    return render(
        request,
        "melding/verzonden.html",
        {
            "signaal": signaal,
            "meldingen_signaal": meldingen_signaal,
        },
    )


@user_passes_test(lambda u: u.is_superuser)
def melding_aangemaakt_email(request, signaal_uuid):
    signaal = get_object_or_404(Signaal, uuid=signaal_uuid)
    meldingen_signaal_response = MeldingenService().signaal_ophalen(
        signaal.meldingen_signaal_url
    )
    meldingen_signaal = {}
    if meldingen_signaal_response.status_code == 200:
        meldingen_signaal = meldingen_signaal_response.json()

    melding_ophalen_response = MeldingenService().melding_ophalen(
        meldingen_signaal.get("_links", {}).get("melding")
    )
    melding = melding_ophalen_response.json()

    email_html_content = MailService().melding_aangemaakt_email(signaal, melding)
    return HttpResponse(email_html_content)


@user_passes_test(lambda u: u.is_superuser)
def melding_afgesloten_email(request, signaal_uuid):
    signaal = get_object_or_404(Signaal, uuid=signaal_uuid)
    meldingen_signaal_response = MeldingenService().signaal_ophalen(
        signaal.meldingen_signaal_url
    )
    meldingen_signaal = {}
    if meldingen_signaal_response.status_code == 200:
        meldingen_signaal = meldingen_signaal_response.json()

    melding_ophalen_response = MeldingenService().melding_ophalen(
        meldingen_signaal.get("_links", {}).get("melding")
    )
    melding = melding_ophalen_response.json()

    email_html_content = MailService().melding_afgesloten_email(signaal, melding)
    return HttpResponse(email_html_content)
