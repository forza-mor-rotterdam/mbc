BEGRAAFPLAATS_CROOSWIJK = ("begraafplaats_crooswijk", "Begraafplaats Crooswijk")
BEGRAAFPLAATS_HOEK_VAN_HOLLAND = (
    "begraafplaats_hoek_van_holland",
    "Begraafplaats Hoek van Holland",
)
BEGRAAFPLAATS_HOFWIJK = (
    "begraafplaats_hofwijk",
    "Begraafplaats en crematorium Hofwijk",
)
BEGRAAFPLAATS_OUDE_LAND = (
    "begraafplaats_oude_land",
    "Begraafplaats Oudeland, Hoogvliet",
)
BEGRAAFPLAATS_OUD_HOOGVLIET = (
    "begraafplaats_oud_hoogvliet",
    "Begraafplaats Oud-Hoogvliet",
)
BEGRAAFPLAATS_OUD_OVERSCHIE = (
    "begraafplaats_oud_overschie",
    "Begraafplaats Oud-Overschie",
)
BEGRAAFPLAATS_OUD_PERNIS = ("begraafplaats_oud_pernis", "Begraafplaats Oud-Pernis")
BEGRAAFPLAATS_OUD_SCHIEBROEK = (
    "begraafplaats_oud_schiebroek",
    "Begraafplaats Oud-Schiebroek",
)
BEGRAAFPLAATS_PERNIS = ("begraafplaats_pernis", "Begraafplaats Pernis")
BEGRAAFPLAATS_ROZENBURG = ("begraafplaats_rozenburg", "Begraafplaats Rozenburg")
BEGRAAFPLAATS_ZUIDERBEGRAAFPLAATS = (
    "begraafplaats_zuiderbegraafplaats",
    "De Zuiderbegraafplaats",
)

BEGRAAFPLAATSEN = (
    (
        BEGRAAFPLAATS_CROOSWIJK,
        (
            ("Collega_A_Crooswijk", "Collega A Crooswijk"),
            ("Collega_B_Crooswijk", "Collega B Crooswijk"),
            ("Collega_C_Crooswijk", "Collega C Crooswijk"),
        ),
    ),
    (
        BEGRAAFPLAATS_HOEK_VAN_HOLLAND,
        (
            "Collega A HvH",
            "Collega B",
            "Collega C",
        ),
    ),
    (
        BEGRAAFPLAATS_HOFWIJK,
        (
            "Collega A Hofwijk",
            "Collega B",
            "Collega C",
        ),
    ),
    (
        BEGRAAFPLAATS_OUDE_LAND,
        (
            "Collega A Oude Land",
            "Collega B",
            "Collega C",
        ),
    ),
    (
        BEGRAAFPLAATS_OUD_HOOGVLIET,
        (
            "Collega A Oud Hoogvliet",
            "Collega B",
            "Collega C",
        ),
    ),
    (
        BEGRAAFPLAATS_OUD_OVERSCHIE,
        (
            "Collega A Oud Overschie",
            "Collega B",
            "Collega C",
        ),
    ),
    (
        BEGRAAFPLAATS_OUD_PERNIS,
        (
            "Collega A Oud Pernis",
            "Collega B",
            "Collega C",
        ),
    ),
    (
        BEGRAAFPLAATS_OUD_SCHIEBROEK,
        (
            "Collega A Oud Schiebroek",
            "Collega B",
            "Collega C",
        ),
    ),
    (
        BEGRAAFPLAATS_PERNIS,
        (
            "Collega A Pernis",
            "Collega B",
            "Collega C",
        ),
    ),
    (
        BEGRAAFPLAATS_ROZENBURG,
        (
            "Collega A Rozenburg",
            "Collega B",
            "Collega C",
        ),
    ),
    (
        BEGRAAFPLAATS_ZUIDERBEGRAAFPLAATS,
        (
            "Collega A Zuiderbegraafplaats",
            "Collega B",
            "Collega C",
        ),
        "bc_crooswijk@rotterdam.nl",
    ),
)

BEGRAAFPLAATS_MEDEWERKERS = {b[0]: b[1] for b in BEGRAAFPLAATSEN}
BEGRAAFPLAATS_EMAIL_ADRES = {b[0]: b[2] for b in BEGRAAFPLAATSEN}
BEGRAAFPLAATS_MEDEWERKERS = {b[0][0]: b[1] for b in BEGRAAFPLAATSEN}

BEGRAAFPLAATS_SELECT = [b[0] for b in BEGRAAFPLAATSEN]

# crooswijk_medewerkers = BEGRAAFPLAATS_MEDEWERKERS[BEGRAAFPLAATS_CROOSWIJK]
