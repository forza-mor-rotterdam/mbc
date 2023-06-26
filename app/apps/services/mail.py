import base64
import logging

from apps.mbc.models import Begraafplaats, Categorie
from apps.services.meldingen import MeldingenService
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

logger = logging.getLogger(__name__)


class MailService:
    def melding_aangemaakt_email(
        self, signaal, melding=None, template_stijl="html", verzenden=False
    ):
        if not melding:
            melding = MeldingenService().melding_ophalen_met_signaal_url(
                signaal.meldingen_signaal_url
            )
        send_to = []
        begraafplaats_id = melding.get("locaties_voor_melding", [])[0].get(
            "begraafplaats"
        )
        begraafplaats = Begraafplaats.objects.get(pk=begraafplaats_id)
        onderwerpen = signaal.formulier_data.get("meta", {}).get("categorie")
        bijlagen = signaal.formulier_data.get("bijlagen", {})
        onderwerpen_list = []
        bijlagen_list = []
        for onderwerp in onderwerpen:
            onderwerpen_list.append(Categorie.objects.get(pk=onderwerp).naam)
        for bijlage in bijlagen:
            bijlagen_list.append(
                "<img src='data:image/jpg;base64,"
                + bijlage["bestand"]
                + "' width='300'>"
            )
        onderwerpen_verbose = ", ".join(onderwerpen_list)
        bijlagen_verbose = ", ".join(bijlagen_list)
        email_context = {
            "melding": melding,
            "begraafplaats": begraafplaats,
            "signaal": signaal,
            "onderwerpen": onderwerpen_verbose,
            "bijlagen": bijlagen_verbose,
            "bijlagen_list": bijlagen,
        }
        if begraafplaats.email:
            send_to.append(begraafplaats.email)
        if signaal.formulier_data.get("melder", {}).get("email"):
            send_to.append(signaal.formulier_data.get("melder", {}).get("email"))

        text_template = get_template("email/email_melding_aanmaken.txt")
        html_template = get_template("email/email_melding_aanmaken.html")
        text_content = text_template.render(email_context)
        html_content = html_template.render(email_context)
        subject = f"Begraafplaats {begraafplaats.naam} - melding aangemaakt"
        msg = EmailMultiAlternatives(
            subject, text_content, settings.DEFAULT_FROM_EMAIL, send_to
        )
        msg.attach_alternative(html_content, "text/html")

        if send_to and not settings.DEBUG and verzenden:
            msg.send()
        if template_stijl == "html":
            return html_content
        return text_content

    def melding_afgesloten_email(
        self, signaal, melding=None, template_stijl="html", verzenden=False
    ):
        if not melding:
            melding = MeldingenService().melding_ophalen_met_signaal_url(
                signaal.meldingen_signaal_url
            )
        logger.info("melding")
        logger.info(melding)
        send_to = []
        begraafplaats_id = melding.get("locaties_voor_melding", [])[0].get(
            "begraafplaats"
        )
        begraafplaats = Begraafplaats.objects.get(pk=begraafplaats_id)

        melding_bijlagen = [
            [
                bijlage.get("afbeelding")
                for bijlage in meldinggebeurtenis.get("bijlagen", [])
            ]
            + [
                b.get("afbeelding")
                for b in (
                    meldinggebeurtenis.get("taakgebeurtenis", {}).get("bijlagen", [])
                    if meldinggebeurtenis.get("taakgebeurtenis")
                    else []
                )
            ]
            for meldinggebeurtenis in melding.get("meldinggebeurtenissen", [])
        ]
        bijlagen_flat = [b for bl in melding_bijlagen for b in bl]
        bijlagen_base64 = []

        for bijlage in bijlagen_flat:
            bijlage_response = MeldingenService().afbeelding_ophalen(bijlage)
            base64_encoded_data = base64.b64encode(bijlage_response.content)
            base64_message = base64_encoded_data.decode("utf-8")
            bijlagen_base64.append(
                f"<img src='data:image/jpg;base64,{base64_message}' width='300'>"
            )

        email_context = {
            "melding": melding,
            "begraafplaats": begraafplaats,
            "signaal": signaal,
            "onderwerpen": ", ".join(
                [o.get("naam") for o in melding.get("onderwerpen", [])]
            ),
            "bijlagen": bijlagen_base64,
        }
        if begraafplaats.email:
            send_to.append(begraafplaats.email)
        if signaal.formulier_data.get("melder", {}).get("email"):
            send_to.append(signaal.formulier_data.get("melder", {}).get("email"))

        text_template = get_template("email/melding_behandeld.txt")
        html_template = get_template("email/melding_behandeld.html")
        text_content = text_template.render(email_context)
        html_content = html_template.render(email_context)
        subject = f"Begraafplaats {begraafplaats.naam} - melding behandeld"
        msg = EmailMultiAlternatives(
            subject, text_content, settings.DEFAULT_FROM_EMAIL, send_to
        )
        msg.attach_alternative(html_content, "text/html")

        if send_to and not settings.DEBUG and verzenden:
            msg.send()
        if template_stijl == "html":
            return html_content
        return text_content
