from apps.signalen.models import Signaal
from rest_framework import serializers


class SignaalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signaal
        fields = "__all__"
