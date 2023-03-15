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
        widget=Select(
            attrs={
                "class": "form-select",
            }
        ),
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
        label="Grafnummer of colombarium",
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
        label="Naam overledene",
        required=True,
    )

    categorie = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-check-input",
                "data-action": "request#toggleInputOtherCategory",
            }
        ),
        label="Categorie",
        choices=CATEGORIE,
        required=True,
    )

    # categorie_omschrijving = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control hidden",
    #             "data-request-target": "categoryDescription",
    #         }
    #     ),
    #     label="Andere oorzaken",
    #     # required=True,
    #     # show_hidden_initial=True,
    # )

    toelichting = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": "4",
            }
        ),
        label="Toelichting",
        required=False,
    )

    aannemer = forms.ChoiceField(
        widget=Select(
            attrs={
                "class": "form-select",
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
        widget=forms.TextInput(attrs={"class": "form-control", "type": "tel"}),
        label="Telefoonnummer",
        required=True,
    )

    email_melder = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "type": "email"}),
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
        if self.data.get("begraafplaats"):
            aannemer_choices = BEGRAAFPLAATS_MEDEWERKERS[self.data["begraafplaats"]]
        self.fields["aannemer"].choices = aannemer_choices
