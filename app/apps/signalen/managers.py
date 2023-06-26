import datetime
import logging

from apps.services.mail import MailService
from apps.services.meldingen import MeldingenService
from django.contrib.gis.db import models
from django.db import OperationalError, transaction
from django.dispatch import Signal as DjangoSignal
from rest_framework.reverse import reverse

logger = logging.getLogger(__name__)


aangemaakt = DjangoSignal()
melding_afgesloten = DjangoSignal()


class SignaalManager(models.Manager):
    class SignaalInGebruik(Exception):
        ...

    class MeldingIsNietAfgeslotenFout(Exception):
        ...

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

            MailService().melding_aangemaakt_email(
                signaal=signaal,
                verzenden=True,
            )

            transaction.on_commit(
                lambda: aangemaakt.send_robust(
                    sender=self.__class__,
                    signaal=signaal,
                )
            )
        return signaal

    def melding_afgesloten(self, signaal, db="default"):
        from apps.signalen.models import Signaal

        with transaction.atomic():
            try:
                locked_signaal = (
                    Signaal.objects.using(db)
                    .select_for_update(nowait=True)
                    .get(pk=signaal.pk)
                )
            except OperationalError:
                raise SignaalManager.SignaalInGebruik

            melding = MeldingenService().melding_ophalen_met_signaal_url(
                locked_signaal.meldingen_signaal_url
            )

            if not melding.get("afgesloten_op"):
                raise SignaalManager.MeldingIsNietAfgeslotenFout()

            try:
                locked_signaal.afgesloten_op = datetime.datetime.strptime(
                    melding.get("afgesloten_op"), "%Y-%m-%dT%H:%M:%S.%f%z"
                )
            except Exception:
                try:
                    locked_signaal.afgesloten_op = datetime.datetime.strptime(
                        melding.get("afgesloten_op"), "%Y-%m-%dT%H:%M:%S%z"
                    )
                except Exception:
                    raise SignaalManager.MeldingIsNietAfgeslotenFout()

            locked_signaal.save()

            MailService().melding_afgesloten_email(
                melding=melding,
                signaal=locked_signaal,
                verzenden=True,
            )

            transaction.on_commit(
                lambda: melding_afgesloten.send_robust(
                    sender=self.__class__,
                    signaal=locked_signaal,
                )
            )
