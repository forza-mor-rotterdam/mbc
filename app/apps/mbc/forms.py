import base64
import copy

import requests
from apps.mbc.models import Begraafplaats, Categorie, Medewerker
from django import forms
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils import timezone


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
        widget=forms.Select(
            attrs={"data-action": "change->request#onBegraafplaatsChange"}
        ),
        label="Begraafplaats",
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
        required=False,
    )
    naam_overledene = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
        help_text='<span>Bekijk namen en graven op <a href="https://grafzoeken.nl/#/0599" target="_blank">grafzoeken.nl</a></span>',
        label="Naam overledene",
        required=True,
    )

    categorie = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-check-input",
            }
        ),
        label="Categorie",
        required=True,
    )

    toelichting = forms.CharField(
        widget=forms.Textarea(),
        label="Toelichting",
        required=True,
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
        widget=forms.Select(
            attrs={
                "data-request-target": "aannemerField",
            }
        ),
        label="Wie heeft het verzoek aangenomen?",
        required=True,
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
        required=False,
    )

    email_melder = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
            }
        ),
        label="E-mailadres",
        required=True,
    )

    no_email = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                "data-action": "change->request#toggleInputNoEmail",
            }
        ),
        label="De melder beschikt niet over een e-mailadres.",
        required=False,
    )

    rechthebbende = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={
                "class": "list--form-radio-input",
            }
        ),
        label="Is deze persoon de rechthebbende of belanghebbende?",
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

    def get_begraafplaats_choices(self):
        return [("", "Selecteer een begraafplaats")] + [
            (str(m[0]), m[1])
            for m in list(Begraafplaats.objects.all().values_list("pk", "naam"))
        ]

    def get_alle_medewerker_choices(self):
        return [("", "Selecteer een medewerker")] + [
            (str(m[0]), m[1])
            for m in list(Medewerker.objects.all().values_list("pk", "naam"))
            + [("onbekend", "Onbekend")]
        ]

    def get_medewerker_choices(self, begraafplaats_id):
        return (
            [("", "Selecteer een medewerker")]
            + [
                (str(m[0]), m[1])
                for m in list(
                    Medewerker.objects.filter(
                        begraafplaatsen__pk=begraafplaats_id
                    ).values_list("pk", "naam")
                )
            ]
            + [("onbekend", "Onbekend")]
        )

    def get_categorie_choices(self):
        return [
            (str(m[0]), m[1])
            for m in list(
                Categorie.objects.all().order_by("volgorde").values_list("pk", "naam")
            )
        ]

    def get_begraafplaats_medewerkers(self):
        medewerkers = list(
            Medewerker.objects.all().values_list("pk", "naam", "begraafplaatsen")
        )
        begraafplaatsen = list(Begraafplaats.objects.all().values_list("pk", flat=True))
        return {
            b: [("", "Selecteer een medewerker")]
            + [(str(m[0]), m[1]) for m in medewerkers if b == m[2]]
            + [("onbekend", "Onbekend")]
            for b in begraafplaatsen
        }

    def get_categorie_andere_oorzaak(self):
        return list(
            [
                str(c)
                for c in Categorie.objects.filter(toon_andere_oorzaak=True).values_list(
                    "pk", flat=True
                )
            ]
        )

    def get_specifiek_graf_categorieen(self):
        return {
            0: list(
                [
                    str(c)
                    for c in Categorie.objects.filter(
                        toon_specifiek_graf__in=("altijd", "niet_specifiek_graf")
                    ).values_list("pk", flat=True)
                ]
            ),
            1: list(
                [
                    str(c)
                    for c in Categorie.objects.filter(
                        toon_specifiek_graf__in=("altijd", "specifiek_graf")
                    ).values_list("pk", flat=True)
                ]
            ),
        }

    def get_verbose_value_from_field(self, fieldname, value):
        if hasattr(self.fields.get(fieldname), "choices"):
            choices_lookup = {c[0]: c[1] for c in self.fields[fieldname].choices}
            if type(value) == list:
                return [choices_lookup.get(v, v) for v in value]
            return choices_lookup.get(value, value)
        return value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["begraafplaats"].choices = self.get_begraafplaats_choices()
        self.fields["categorie"].choices = self.get_categorie_choices()

        if "categorie_andere_oorzaken" in self.data.get("categorie", []):
            self.fields["omschrijving_andere_oorzaken"].required = True

        if "0" in self.data.get("specifiek_graf", []):
            self.fields["naam_overledene"].required = False
            self.fields["grafnummer"].required = False
            self.fields["rechthebbende"].required = False

        if self.data.get("begraafplaats"):
            self.fields["aannemer"].choices = self.get_medewerker_choices(
                self.data["begraafplaats"]
            )
            self.fields["aannemer"].required = False

    def send_mail(self, files=[]):
        email_context = copy.deepcopy(self.cleaned_data)
        send_to = []
        begraafplaats = Begraafplaats.objects.get(pk=email_context["begraafplaats"])
        if begraafplaats.email:
            send_to.append(begraafplaats.email)
        if email_context.get("email_melder"):
            send_to.append(email_context.get("email_melder"))

        email_context["fotos"] = len(files)
        choice_fields = (
            "categorie",
            "begraafplaats",
            "aannemer",
            "terugkoppeling_gewenst",
            "rechthebbende",
            "specifiek_graf",
        )
        for cf in choice_fields:
            email_context[cf] = self.get_verbose_value_from_field(cf, email_context[cf])

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
        print(post_data)
        post_data["bijlagen"] = [{"bestand": self._to_base64(file)} for file in files]

        response = requests.post(url, json=post_data)
        response.raise_for_status()
