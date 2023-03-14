BEGRAAFPLAATS_CROOSWIJK = "Crooswijk"

BEGRAAFPLAATSEN = (
    (
        BEGRAAFPLAATS_CROOSWIJK,
        (
            "Collega A",
            "Collega B",
            "Collega C",
        ),
    ),
)

BEGRAAFPLAATS_MEDEWERKERS = {b[0]: b[1] for b in BEGRAAFPLAATSEN}

# crooswijk_medewerkers = BEGRAAFPLAATS_MEDEWERKERS[BEGRAAFPLAATS_CROOSWIJK]
