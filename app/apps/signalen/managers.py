import logging

from apps.services.meldingen import MeldingenService
from django.contrib.gis.db import models
from django.db import transaction
from django.dispatch import Signal as DjangoSignal
from rest_framework.reverse import reverse

logger = logging.getLogger(__name__)


aangemaakt = DjangoSignal()


class SignaalManager(models.Manager):
    class MeldingenSignaalAanmakenFout(Exception):
        ...

    def signaal_aanmaken(self, signaal_data, request, db="default"):
        from apps.signalen.models import Signaal

        with transaction.atomic():
            meldingen_data = {}
            meldingen_data.update(signaal_data)
            signaal = Signaal.objects.create(
                formulier_data=signaal_data,
            )
            signaal_data.update(
                {
                    "signaal_url": reverse(
                        "v1:signaal-detail",
                        kwargs={"uuid": signaal.uuid},
                        request=request,
                    )
                }
            )
            signaal_response = MeldingenService().signaal_aanmaken(
                data=signaal_data,
            )
            if signaal_response.status_code == 201:
                signaal.meldingen_signaal_url = (
                    signaal_response.json().get("_links", {}).get("self")
                )
            else:
                raise SignaalManager.MeldingenSignaalAanmakenFout(
                    f"response status code: {signaal_response.status_code}, response tekst: {signaal_response.text}"
                )

            signaal.save()
            transaction.on_commit(
                lambda: aangemaakt.send_robust(
                    sender=self.__class__,
                    signaal=signaal,
                )
            )
