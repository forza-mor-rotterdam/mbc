import base64
import copy

import requests
from apps.mbc.constanten import (
    ALLE_MEDEWERKERS,
    BEGRAAFPLAATS_EMAIL_ADRES,
    BEGRAAFPLAATS_MEDEWERKER_NAAM,
    BEGRAAFPLAATS_MEDEWERKERS,
    BEGRAAFPLAATS_NAAM,
    BEGRAAFPLAATS_SELECT,
    CATEGORIE,
    CATEGORIE_NAAM,
)
from django import forms
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils import timezone


class Select(forms.Select):
    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if not option.get("value"):
            option["attrs"]["disabled"] = "disabled"

        if option.get("value") == 2:
            option["attrs"]["disabled"] = "disabled"

        return option


class MeldingAanmakenForm(forms.Form):

    specifiek_graf = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={
                "class": "list--form-radio-input",
                "data-action": "change->request#onSpecifiekGrafChange",
                "data-request-target": "specifiekGrafField",
            }
        ),
        label="Betreft het verzoek een specifiek graf?",
        choices=(
            ("1", "Ja"),
            ("0", "Nee"),
        ),
        required=True,
    )
    begraafplaats = forms.ChoiceField(
        widget=Select(attrs={"data-action": "change->request#onBegraafplaatsChange"}),
        label="Begraafplaats",
        choices=BEGRAAFPLAATS_SELECT,
        required=True,
    )
    grafnummer = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        label="Grafnummer",
        required=True,
    )
    vak = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        label="Vak",
        required=True,
    )
    naam_overledene = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        help_text='<span>Bekijk namen en graven op <a href="https://grafzoeken.nl/" target="_blank">grafzoeken.nl</a></span>',
        label="Naam overledene",
        required=True,
    )

    categorie = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-check-input",
                "data-action": "change->request#toggleInputOtherCategory",
            }
        ),
        label="Categorie",
        choices=CATEGORIE,
        required=True,
    )
    omschrijving_andere_oorzaken = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "data-request-target": "categorieOmschrijvingField",
            }
        ),
        label="Omschrijving andere oorzaken",
        required=False,
    )
    toelichting = forms.CharField(
        widget=forms.Textarea(),
        label="Toelichting",
        required=False,
    )

    fotos = forms.FileField(
        widget=forms.widgets.FileInput(
            attrs={
                "accept": ".jpg, .jpeg, .png",
                "data-action": "change->request#updateImageDisplay",
            }
        ),
        label="Foto's",
        required=False,
    )
    aannemer = forms.ChoiceField(
        widget=Select(
            attrs={
                "data-request-target": "aannemerField",
            }
        ),
        label="Wie heeft het verzoek aangenomen?",
        choices=ALLE_MEDEWERKERS,
        required=False,
    )

    naam_melder = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        label="Naam",
        required=True,
    )

    telefoon_melder = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "class": "form-control",
            }
        ),
        label="Telefoonnummer",
        required=True,
    )

    email_melder = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
            }
        ),
        label="E-mailadres",
        required=False,
    )

    rechthebbende = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={
                "class": "list--form-radio-input",
            }
        ),
        label="Is deze persoon de rechthebbende?",
        choices=(
            ("1", "Ja"),
            ("0", "Nee"),
            ("2", "Onbekend"),
        ),
        required=True,
    )

    terugkoppeling_gewenst = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={
                "class": "list--form-radio-input",
            }
        ),
        label="Is terugkoppeling gewenst?",
        choices=(
            ("1", "Ja"),
            ("0", "Nee"),
        ),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aannemer_choices = ALLE_MEDEWERKERS
        if "categorie_andere_oorzaken" in self.data.get("categorie", []):
            self.fields["omschrijving_andere_oorzaken"].required = True

        if "0" in self.data.get("specifiek_graf", []):
            self.fields["naam_overledene"].required = False
            self.fields["grafnummer"].required = False
            self.fields["rechthebbende"].required = False

        if self.data.get("begraafplaats"):
            aannemer_choices = BEGRAAFPLAATS_MEDEWERKERS[self.data["begraafplaats"]]
        self.fields["aannemer"].choices = aannemer_choices
        self.fields["aannemer"].required = False

    def send_mail(self, files=[]):
        email_context = copy.deepcopy(self.cleaned_data)
        send_to = []
        if BEGRAAFPLAATS_EMAIL_ADRES.get(self.cleaned_data.get("begraafplaats")):
            send_to.append(
                BEGRAAFPLAATS_EMAIL_ADRES.get(self.cleaned_data.get("begraafplaats"))
            )
        if self.cleaned_data.get("email_melder"):
            send_to.append(self.cleaned_data.get("email_melder"))

        email_context["fotos"] = len(files)
        email_context["categorie"] = ", ".join(
            [CATEGORIE_NAAM[c] for c in email_context["categorie"]]
        )
        email_context["begraafplaats"] = BEGRAAFPLAATS_NAAM[
            email_context["begraafplaats"]
        ]
        email_context["aannemer"] = BEGRAAFPLAATS_MEDEWERKER_NAAM[
            email_context["aannemer"]
        ]

        text_template = get_template("email/email.txt")
        html_template = get_template("email/email.html")
        text_content = text_template.render(email_context)
        html_content = html_template.render(email_context)
        subject = "Serviceverzoek Begraven & Cremeren"
        msg = EmailMultiAlternatives(
            subject, text_content, settings.DEFAULT_FROM_EMAIL, send_to
        )
        msg.attach_alternative(html_content, "text/html")
        for f in files:
            msg.attach(f.name, f.read(), f.content_type)
        if send_to and not settings.DEBUG:
            msg.send()

    def _to_base64(self, file):
        binary_file = default_storage.open(file)
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_message = base64_encoded_data.decode("utf-8")
        return base64_message

    def send_to_meldingen(self, files=[], request=None):
        now = timezone.localtime(timezone.now())
        url = f"{settings.MELDINGEN_API}/signaal/"
        data = self.cleaned_data
        data.pop("fotos")
        labels = {
            k: {
                "label": v.label,
                "choices": {c[0]: c[1] for c in v.choices}
                if hasattr(v, "choices")
                else None,
            }
            for k, v in self.fields.items()
        }
        data.update(
            {
                "labels": labels,
            }
        )
        post_data = {
            "melder": {
                "naam": data.get("naam_melder"),
                "email": data.get("email_melder"),
                "telefoonnummer": data.get("telefoon_melder"),
            },
            "origineel_aangemaakt": now.isoformat(),
            "bron": f"{request.build_absolute_uri('/api/melding/id')}"
            if request
            else "link-to-source",
            "onderwerp": "Begraven & cremeren",
            "ruwe_informatie": data,
        }
        post_data["bijlagen"] = [{"bestand": self._to_base64(file)} for file in files]

        response = requests.post(url, json=post_data)
        response.raise_for_status()