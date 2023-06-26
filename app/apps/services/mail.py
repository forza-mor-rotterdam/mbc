import base64
import logging
import os.path
import re

import magic
from apps.mbc.models import Begraafplaats, Categorie
from apps.services.meldingen import MeldingenService
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import EmailMultiAlternatives, SafeMIMEMultipart
from django.template.loader import get_template

logger = logging.getLogger(__name__)


class EmailMultiRelated(EmailMultiAlternatives):
    """
    A version of EmailMessage that makes it easy to send multipart/related
    messages. For example, including text and HTML versions with inline images.

    @see https://djangosnippets.org/snippets/2215/
    """

    related_subtype = "related"

    def __init__(self, *args, **kwargs):
        # self.related_ids = []
        self.related_attachments = []
        return super().__init__(*args, **kwargs)

    def attach_related(self, filename, content, mimetype):
        self.related_attachments.append((filename, content, mimetype))

    def attach_related_file(self, path):
        """Attaches a file from the filesystem."""
        filename = os.path.basename(path)
        content = open(path, "rb").read()
        mime = magic.Magic(mime=True)
        mimetype = mime.from_file(path)
        self.attach_related(filename, content, mimetype)

    def _create_message(self, msg):
        return self._create_attachments(
            self._create_related_attachments(self._create_alternatives(msg))
        )

    def _create_alternatives(self, msg):
        for i, (content, mimetype) in enumerate(self.alternatives):
            if mimetype == "text/html":
                for related_attachment in self.related_attachments:
                    filename, _, _ = related_attachment
                    content = re.sub(
                        r"(?<!cid:)%s" % re.escape(filename),
                        "cid:%s" % filename,
                        content,
                    )
                self.alternatives[i] = (content, mimetype)

        return super()._create_alternatives(msg)

    def _create_related_attachments(self, msg):
        encoding = self.encoding or settings.DEFAULT_CHARSET
        if self.related_attachments:
            body_msg = msg
            msg = SafeMIMEMultipart(_subtype=self.related_subtype, encoding=encoding)
            if self.body:
                msg.attach(body_msg)
            for related_attachment in self.related_attachments:
                msg.attach(self._create_related_attachment(*related_attachment))
        return msg

    def _create_related_attachment(self, filename, content, mimetype=None):
        """
        Convert the filename, content, mimetype triple into a MIME attachment
        object. Adjust headers to use Content-ID where applicable.
        Taken from http://code.djangoproject.com/ticket/4771
        """
        attachment = super()._create_attachment(filename, content, mimetype)
        if filename:
            mimetype = attachment["Content-Type"]
            del attachment["Content-Type"]
            del attachment["Content-Disposition"]
            attachment.add_header("Content-Disposition", "inline", filename=filename)
            attachment.add_header("Content-Type", mimetype, name=filename)
            attachment.add_header("Content-ID", "<%s>" % filename)
        return attachment


class MailService:
    def melding_aangemaakt_email(
        self,
        signaal,
        melding=None,
        template_stijl="html",
        verzenden=False,
        bestanden=[],
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
        email_context = {
            "melding": melding,
            "begraafplaats": begraafplaats,
            "signaal": signaal,
            "onderwerpen": onderwerpen_verbose,
            "bijlagen": bestanden,
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
        msg = EmailMultiRelated(
            subject, text_content, settings.DEFAULT_FROM_EMAIL, send_to
        )
        msg.attach_alternative(html_content, "text/html")

        for f in bestanden:
            attachment = default_storage.path(f)
            print(attachment)
            msg.attach_related_file(attachment)

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
