import magic
from apps.mbc.models import Begraafplaats, Categorie
from apps.services.meldingen import MeldingenService
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


class MailService:
    def melding_aangemaakt_email(self, signaal, melding, template_stijl="html"):
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
                "<img src='data:image/png;base64, "
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
        if template_stijl == "html":
            return html_content
        return text_content

    def melding_afgesloten_email(self, signaal, melding, template_stijl="html"):
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
                "<img src='data:image/png;base64, "
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
        if template_stijl == "html":
            return html_content
        return text_content
