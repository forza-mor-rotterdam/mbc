from apps.mbc.constanten import (
    ALLE_MEDEWERKERS,
    BEGRAAFPLAATS_MEDEWERKERS,
    BEGRAAFPLAATS_SELECT,
    CATEGORIE,
)
from django import forms


class RadioSelect(forms.RadioSelect):
    option_template_name = "widgets/radio_option.html"


class Select(forms.Select):
    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if not option.get("value"):
            option["attrs"]["disabled"] = "disabled"

        if option.get("value") == 2:
            option["attrs"]["disabled"] = "disabled"

        return option


class MeldingAanmakenForm(forms.Form):
    begraafplaats = forms.ChoiceField(
        widget=Select(attrs={"data-action": "change->request#onChangeSendForm"}),
        label="Begraafplaats",
        choices=BEGRAAFPLAATS_SELECT,
        required=True,
    )
    grafnummer = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Grafnummer",
        required=True,
    )
    vak = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Vak",
        required=True,
    )
    naam_overledene = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Naam overledene",
        required=True,
    )

    categorie = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-check-input",
                "data-action": "change->request#onChangeSendForm",
            }
        ),
        label="Categorie",
        choices=CATEGORIE,
        required=True,
    )
    omschrijving_andere_oorzaken = forms.CharField(
        widget=forms.HiddenInput(),
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
        widget=Select(),
        label="Wie heeft het verzoek aangenomen?",
        choices=ALLE_MEDEWERKERS,
        required=False,
    )

    naam_melder = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Naam",
        required=True,
    )

    telefoon_melder = forms.CharField(
        widget=forms.TextInput(attrs={"type": "tel", "class": "form-control"}),
        label="Telefoonnummer",
        required=True,
    )

    email_melder = forms.CharField(
        widget=forms.TextInput(attrs={"type": "email", "class": "form-control"}),
        label="E-mailadres",
        required=False,
    )

    rechthebbende = forms.ChoiceField(
        widget=RadioSelect(
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
        widget=RadioSelect(
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
            self.fields["omschrijving_andere_oorzaken"].widget = forms.TextInput(
                attrs={"class": "form-control", "required": "required"}
            )
            self.fields["omschrijving_andere_oorzaken"].required = True

        if self.data.get("begraafplaats"):
            aannemer_choices = BEGRAAFPLAATS_MEDEWERKERS[self.data["begraafplaats"]]
        self.fields["aannemer"].choices = aannemer_choices
