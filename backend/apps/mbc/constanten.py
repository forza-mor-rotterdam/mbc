BEGRAAFPLAATS_CROOSWIJK = "Crooswijk"

BEGRAAFPLAATSEN = (
    (
        BEGRAAFPLAATS_CROOSWIJK,
        (
            "Collega A",
            "Collega B",
            "Collega C",
        ),
        "bc_crooswijk@rotterdam.nl",
    ),
)

BEGRAAFPLAATS_MEDEWERKERS = {b[0]: b[1] for b in BEGRAAFPLAATSEN}
BEGRAAFPLAATS_EMAIL_ADRES = {b[0]: b[2] for b in BEGRAAFPLAATSEN}

# crooswijk_medewerkers = BEGRAAFPLAATS_MEDEWERKERS[BEGRAAFPLAATS_CROOSWIJK]
