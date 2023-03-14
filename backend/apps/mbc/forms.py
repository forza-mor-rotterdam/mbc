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
    fieldsets = (
        {
            "titel": "Fieldset naam",
            "icon": "Fieldset icon",
            "fields": (
                "begraafplaats",
                "naam_melder",
            ),
        },
        {},
    )

    begraafplaats = forms.ChoiceField(
        widget=Select(
            attrs={
                "class": "form-select",
            }
        ),
        label="Begraafplaats",
        choices=(
            ("", "Selecteer een begraafplaats"),
            ("begraafplaats_crooswijk", "Begraafplaats Crooswijk"),
            ("begraafplaats_hoek_van_holland", "Begraafplaats Hoek van Holland"),
            ("begraafplaats_hofwijk", "Begraafplaats en crematorium Hofwijk"),
            ("begraafplaats_oude_land", "Begraafplaats Oudeland, Hoogvliet"),
            ("begraafplaats_oud_hoogvliet", "Begraafplaats Oud-Hoogvliet"),
            ("begraafplaats_oud_overschie", "Begraafplaats Oud-Overschie"),
            ("begraafplaats_oud_pernis", "Begraafplaats Oud-Pernis"),
            ("begraafplaats_oud_schiebroek", "Begraafplaats Oud-Schiebroek"),
            ("begraafplaats_pernis", "Begraafplaats Pernis"),
            ("begraafplaats_rozenburg", "Begraafplaats Rozenburg"),
            ("begraafplaats_zuiderbegraafplaats", "De Zuiderbegraafplaats"),
        ),
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
        choices=(
            ("categorie_verzakking_eigen_graf", "Verzakking eigen graf"),
            ("categorie_verzakking_algemeen", "Verzakking algemeen"),
            ("categorie_snoeien", "Snoeien"),
            ("categorie_beplanting", "Beplanting"),
            ("categorie_schoonmaken", "Schoonmaken"),
            ("categorie_verdwenen_materiaal", "Verdwenen materiaal"),
            ("categorie_gaten", "Gaten"),
            ("categorie_wespennest", "Wespennest"),
            ("categorie_konijnen", "Konijnen"),
            ("categorie_muizen", "Muizen"),
            ("categorie_zerk_reinigen", "Zerk reinigen"),
            ("categorie_andere_oorzaken", "Andere oorzaken"),
        ),
        required=True,
    )

    categorie_omschrijving = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control hidden",
                "data-request-target": "categoryDescription",
            }
        ),
        label="Andere oorzaken",
        required=True,
        show_hidden_initial=True,
    )

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
        choices=(
            ("", "Selecteer een collega"),
            ("collega_onbekend", "Onbekend"),
            ("collega_a", "Collega A"),
            ("collega_b", "Collega B"),
            ("collega_c", "Collega C"),
            ("collega_d", "Collega D"),
            ("collega_e", "Collega E"),
            ("collega_f", "Collega F"),
            ("collega_g", "Collega G"),
        ),
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
