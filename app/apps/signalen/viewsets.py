from apps.signalen.models import Signaal
from apps.signalen.serializers import SignaalSerializer
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class SignaalViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    lookup_field = "uuid"
    queryset = Signaal.objects.all()

    serializer_class = SignaalSerializer

    # @extend_schema(
    #     description="Melding afgesloten notificatie",
    #     request=None,
    #     responses=[status.HTTP_204_NO_CONTENT],
    #     parameters=None,
    # )
    @action(
        detail=True,
        methods=["get"],
        url_path="melding-afgesloten",
    )
    def melding_afgesloten(self, request, uuid):

        Signaal.acties.melding_afgesloten(self.get_object())

        return Response(
            status=status.HTTP_200_OK,
        )
