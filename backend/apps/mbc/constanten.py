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

BEGRAAFPLAATSEN_SOURCE = (
    (
        BEGRAAFPLAATS_CROOSWIJK,
        (
            "Collega A Crooswijk",
            "Collega B Crooswijk",
            "Collega C Crooswijk",
        ),
    ),
    (
        BEGRAAFPLAATS_HOEK_VAN_HOLLAND,
        (
            "Collega D",
            "Collega E",
            "Collega F",
        ),
    ),
    (
        BEGRAAFPLAATS_HOFWIJK,
        (
            "Collega G",
            "Collega H",
            "Collega I",
        ),
    ),
    (
        BEGRAAFPLAATS_OUDE_LAND,
        (
            "Collega J",
            "Collega K",
            "Collega L",
        ),
    ),
    (
        BEGRAAFPLAATS_OUD_HOOGVLIET,
        (
            "Collega M",
            "Collega N",
            "Collega O",
        ),
    ),
    (
        BEGRAAFPLAATS_OUD_OVERSCHIE,
        (
            "Collega P",
            "Collega Q",
            "Collega R",
        ),
    ),
    (
        BEGRAAFPLAATS_OUD_PERNIS,
        (
            "Collega S",
            "Collega T",
            "Collega U",
        ),
    ),
    (
        BEGRAAFPLAATS_OUD_SCHIEBROEK,
        (
            "Collega V",
            "Collega W",
            "Collega X",
        ),
    ),
    (
        BEGRAAFPLAATS_PERNIS,
        (
            "Collega Y",
            "Collega Z",
            "Collega AA",
        ),
    ),
    (
        BEGRAAFPLAATS_ROZENBURG,
        (
            "Collega BB",
            "Collega CC",
            "Collega DD",
        ),
    ),
    (
        BEGRAAFPLAATS_ZUIDERBEGRAAFPLAATS,
        (
            "Collega EE",
            "Collega FF",
            "Collega GG",
        ),
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
CATEGORIE = [[snake_case(c), c] for c in CATEGORIE_SOURCE]
BEGRAAFPLAATSEN = [
    [[snake_case(b[0]), b[0]], [[snake_case(c), c] for c in b[1]]]
    for b in BEGRAAFPLAATSEN_SOURCE
]
ALLE_MEDEWERKERS = [["", "Selecteer een medewerker"]] + [
    m for b in BEGRAAFPLAATSEN for m in b[1]
]
BEGRAAFPLAATS_MEDEWERKERS = {
    b[0][0]: [["", "Selecteer een medewerker"]] + b[1] for b in BEGRAAFPLAATSEN
}
BEGRAAFPLAATS_SELECT = [["", "Selecteer een begraafplaats"]] + [
    b[0] for b in BEGRAAFPLAATSEN
]
