from apps.mbc.utils import snake_case

BEGRAAFPLAATS_CROOSWIJK = "Begraafplaats Crooswijk"
BEGRAAFPLAATS_HOEK_VAN_HOLLAND = "Begraafplaats Hoek van Holland"
BEGRAAFPLAATS_HOFWIJK = "Begraafplaats en crematorium Hofwijk"
BEGRAAFPLAATS_OUDE_LAND = "Begraafplaats Oudeland, Hoogvliet"
BEGRAAFPLAATS_OUD_HOOGVLIET = "Begraafplaats Oud-Hoogvliet"
BEGRAAFPLAATS_OUD_OVERSCHIE = "Begraafplaats Oud-Overschie"
BEGRAAFPLAATS_OUD_PERNIS = "Begraafplaats Oud-Pernis"
BEGRAAFPLAATS_OUD_SCHIEBROEK = "Begraafplaats Oud-Schiebroek"
BEGRAAFPLAATS_PERNIS = "Begraafplaats Pernis"
BEGRAAFPLAATS_ROZENBURG = "Begraafplaats Rozenburg"
BEGRAAFPLAATS_ZUIDERBEGRAAFPLAATS = "De Zuiderbegraafplaats"

DEFAULT_BEGRAAFPLAATS_EMAIL = ""

BEGRAAFPLAATS_MEDEWERKERS_ZUID = (
    "C.M. Hendriks",
    "A. van de Graaf",
    "I. Addicks",
    "A.J. Verhoeven",
    "M. van Berkum",
)

BEGRAAFPLAATSEN_SOURCE = (
    (
        BEGRAAFPLAATS_CROOSWIJK,
        (
            "Collega A Crooswijk",
            "Collega B Crooswijk",
            "Collega C Crooswijk",
        ),
        DEFAULT_BEGRAAFPLAATS_EMAIL,
    ),
    (
        BEGRAAFPLAATS_HOEK_VAN_HOLLAND,
        (
            "Collega D",
            "Collega E",
            "Collega F",
        ),
        DEFAULT_BEGRAAFPLAATS_EMAIL,
    ),
    (
        BEGRAAFPLAATS_HOFWIJK,
        (
            "Collega G",
            "Collega H",
            "Collega I",
        ),
        DEFAULT_BEGRAAFPLAATS_EMAIL,
    ),
    (
        BEGRAAFPLAATS_OUDE_LAND,
        BEGRAAFPLAATS_MEDEWERKERS_ZUID,
        DEFAULT_BEGRAAFPLAATS_EMAIL,
    ),
    (
        BEGRAAFPLAATS_OUD_HOOGVLIET,
        (
            "Collega M",
            "Collega N",
            "Collega O",
        ),
        DEFAULT_BEGRAAFPLAATS_EMAIL,
    ),
    (
        BEGRAAFPLAATS_OUD_OVERSCHIE,
        (
            "Collega P",
            "Collega Q",
            "Collega R",
        ),
        DEFAULT_BEGRAAFPLAATS_EMAIL,
    ),
    (
        BEGRAAFPLAATS_OUD_PERNIS,
        (
            "Collega S",
            "Collega T",
            "Collega U",
        ),
        DEFAULT_BEGRAAFPLAATS_EMAIL,
    ),
    (
        BEGRAAFPLAATS_OUD_SCHIEBROEK,
        (
            "Collega V",
            "Collega W",
            "Collega X",
        ),
        DEFAULT_BEGRAAFPLAATS_EMAIL,
    ),
    (
        BEGRAAFPLAATS_PERNIS,
        BEGRAAFPLAATS_MEDEWERKERS_ZUID,
        DEFAULT_BEGRAAFPLAATS_EMAIL,
    ),
    (
        BEGRAAFPLAATS_ROZENBURG,
        BEGRAAFPLAATS_MEDEWERKERS_ZUID,
        DEFAULT_BEGRAAFPLAATS_EMAIL,
    ),
    (
        BEGRAAFPLAATS_ZUIDERBEGRAAFPLAATS,
        BEGRAAFPLAATS_MEDEWERKERS_ZUID,
        DEFAULT_BEGRAAFPLAATS_EMAIL,
    ),
)

CATEGORIE_SOURCE = [
    "Verzakking eigen graf",
    "Verzakking algemeen",
    "Snoeien",
    "Beplanting",
    "Schoonmaken",
    "Verdwenen materiaal",
    "Gaten",
    "Wespennest",
    "Konijnen",
    "Muizen",
    "Zerk reinigen",
    "Andere oorzaken",
]
CATEGORIE = [[f"categorie_{snake_case(c)}", c] for c in CATEGORIE_SOURCE]
CATEGORIE_NAAM = {c[0]: c[1] for c in CATEGORIE}
BEGRAAFPLAATSEN = [
    [[snake_case(b[0]), b[0]], [[snake_case(c), c] for c in b[1]], b[2]]
    for b in BEGRAAFPLAATSEN_SOURCE
]
BEGRAAFPLAATS_NAAM = {b[0][0]: b[0][1] for b in BEGRAAFPLAATSEN}
ALLE_MEDEWERKERS = [["", "Selecteer een medewerker"]] + [
    m for b in BEGRAAFPLAATSEN for m in b[1]
]
BEGRAAFPLAATS_EMAIL_ADRES = {b[0][0]: b[2] for b in BEGRAAFPLAATSEN}
BEGRAAFPLAATS_MEDEWERKERS = {
    b[0][0]: [["", "Selecteer een medewerker"], ["onbekend", "Onbekend"]] + b[1]
    for b in BEGRAAFPLAATSEN
}
BEGRAAFPLAATS_MEDEWERKER_NAAM = {m[0]: m[1] for b in BEGRAAFPLAATSEN for m in b[1]}
BEGRAAFPLAATS_NAAM = {b[0][0]: b[0][1] for b in BEGRAAFPLAATSEN}
BEGRAAFPLAATS_EMAIL = {b[0][0]: b[2] for b in BEGRAAFPLAATSEN}
BEGRAAFPLAATS_SELECT = [["", "Selecteer een begraafplaats"]] + [
    b[0] for b in BEGRAAFPLAATSEN
]
