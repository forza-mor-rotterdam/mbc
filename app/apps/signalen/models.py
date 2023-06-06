from apps.signalen.managers import SignaalManager
from apps.signalen.querysets import SignaalQuerySet
from django.contrib.gis.db import models
from utils.models import BasisModel


class Signaal(BasisModel):
    meldingen_signaal_url = models.URLField(
        null=True,
        blank=True,
    )
    formulier_data = models.JSONField(default=dict)

    objects = SignaalQuerySet.as_manager()
    acties = SignaalManager()

    def __str__(self) -> str:
        return self.meldingen_signaal_url or self.pk

    class Meta:
        ordering = ("-aangemaakt_op",)
        verbose_name = "Signaal"
        verbose_name_plural = "Signalen"
