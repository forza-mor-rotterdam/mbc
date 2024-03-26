import logging

from apps.main.forms import MeldingAanmakenForm
from apps.services.mail import MailService
from apps.services.meldingen import MeldingenService
from apps.signalen.models import Signaal
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
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


@login_required
def root(request):
    return redirect(reverse("melding_aanmaken"))


@user_passes_test(lambda u: u.is_superuser)
def clear_melding_token_from_cache(request):
    cache.delete("meldingen_token")
    return HttpResponse("melding_token removed from cache")


@login_required
def melding_aanmaken(request):
    session_expiry_max_timestamp = (
        request.session.get("_session_init_timestamp_")
        + settings.SESSION_EXPIRE_MAXIMUM_SECONDS
    )
    session_expiry_timestamp = (
        request.session.get("_session_current_timestamp_")
        + settings.SESSION_EXPIRE_SECONDS
    )
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
            MailService().melding_aangemaakt_email(
                signaal=signaal, verzenden=True, bestanden=file_names
            )
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
            "session_expiry_max_timestamp": session_expiry_max_timestamp,
            "session_expiry_timestamp": session_expiry_timestamp,
        },
    )


@login_required
def melding_verzonden(request, signaal_uuid):
    signaal = get_object_or_404(Signaal, uuid=signaal_uuid)
    meldingen_signaal = MeldingenService().signaal_ophalen(
        signaal.meldingen_signaal_url
    )
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
    template_stijl = request.GET.get("template_stijl", "html")
    email_verzenden = bool(request.GET.get("verzenden", False))
    signaal = get_object_or_404(Signaal, uuid=signaal_uuid)

    email_html_content = MailService().melding_aangemaakt_email(
        signaal, template_stijl=template_stijl, verzenden=email_verzenden
    )
    return HttpResponse(email_html_content)


@user_passes_test(lambda u: u.is_superuser)
def melding_afgesloten_email(request, signaal_uuid):
    template_stijl = request.GET.get("template_stijl", "html")
    email_verzenden = bool(request.GET.get("verzenden", False))
    signaal = get_object_or_404(Signaal, uuid=signaal_uuid)

    email_html_content = MailService().melding_afgesloten_email(
        signaal, template_stijl=template_stijl, verzenden=email_verzenden
    )
    return HttpResponse(email_html_content)
