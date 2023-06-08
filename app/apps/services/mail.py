import magic
from apps.mbc.models import Begraafplaats
from apps.services.meldingen import MeldingenService
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


class MailService:
    def melding_aangemaakt_email(self, signaal, melding):
        send_to = []
        begraafplaats_id = melding.get("locaties_voor_melding", [])[0].get(
            "begraafplaats"
        )
        begraafplaats = Begraafplaats.objects.get(pk=begraafplaats_id)
        email_context = {
            "melding": melding,
            "begraafplaats": begraafplaats,
        }
        if begraafplaats.email:
            send_to.append(begraafplaats.email)
        if signaal.formulier_data.get("melder", {}).get("email"):
            send_to.append(signaal.formulier_data.get("melder", {}).get("email"))

        text_template = get_template("email/email.txt")
        html_template = get_template("email/email.html")
        text_content = text_template.render(email_context)
        html_content = html_template.render(email_context)
        subject = f"Begraafplaats {begraafplaats.naam} - melding behandeld"
        msg = EmailMultiAlternatives(
            subject, text_content, settings.DEFAULT_FROM_EMAIL, send_to
        )
        msg.attach_alternative(html_content, "text/html")

        bijlagen = [
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
        bijlagen_flat = [b for bl in bijlagen for b in bl]

        mime = magic.Magic(mime=True)
        for bijlage in bijlagen_flat:
            filename = bijlage.split("/")[-1]
            bijlage_response = MeldingenService().afbeelding_ophalen(bijlage)
            open(filename, "wb").write(bijlage_response.content)
            msg.attach(filename, bijlage_response.content, mime.from_file(filename))

        if send_to and not settings.DEBUG:
            msg.send()
        return html_content

    def melding_afgesloten_email(self, signaal, melding):
        send_to = []
        begraafplaats_id = melding.get("locaties_voor_melding", [])[0].get(
            "begraafplaats"
        )
        begraafplaats = Begraafplaats.objects.get(pk=begraafplaats_id)
        email_context = {
            "melding": melding,
            "begraafplaats": begraafplaats,
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

        bijlagen = [
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
        bijlagen_flat = [b for bl in bijlagen for b in bl]

        mime = magic.Magic(mime=True)
        for bijlage in bijlagen_flat:
            filename = bijlage.split("/")[-1]
            bijlage_response = MeldingenService().afbeelding_ophalen(bijlage)
            open(filename, "wb").write(bijlage_response.content)
            msg.attach(filename, bijlage_response.content, mime.from_file(filename))

        if send_to and not settings.DEBUG:
            msg.send()
        return html_content
