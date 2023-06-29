from django.contrib.gis.db import models


class Begraafplaats(models.Model):
    naam = models.CharField(max_length=200)
    email = models.EmailField(
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.naam

    class Meta:
        ordering = ("naam",)
        verbose_name_plural = "Begraafplaatsen"


class Medewerker(models.Model):
    naam = models.CharField(max_length=200)
    email = models.EmailField(
        null=True,
        blank=True,
    )
    begraafplaatsen = models.ManyToManyField(
        to="main.Begraafplaats",
        related_name="medewerkers",
    )

    def __str__(self) -> str:
        return self.naam

    class Meta:
        ordering = ("naam",)


class Categorie(models.Model):
    naam = models.CharField(max_length=200)
    volgorde = models.IntegerField(default=0)
    toon_andere_oorzaak = models.BooleanField(default=False)
    toon_specifiek_graf = models.CharField(
        max_length=50,
        help_text="Toon deze categorie als kiest voor een specifiek graf",
        choices=(
            ("altijd", "Altijd tonen"),
            ("specifiek_graf", "Alleen tonen als specifiek graf gekozen is"),
            ("niet_specifiek_graf", "Alleen tonen als specifiek graf niet gekozen is"),
        ),
        default="altijd",
    )
    onderwerp = models.URLField(
        default="https://mor-core-acc.forzamor.nl/v1/onderwerp/overig/"
    )

    def __str__(self) -> str:
        return self.naam

    class Meta:
        ordering = ("volgorde",)
        verbose_name_plural = "Categorieën"
