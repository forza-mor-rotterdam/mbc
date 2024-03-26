import logging

import jwt
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from utils.diversen import absolute

logger = logging.getLogger(__name__)


def general_settings(context):
    oidc_id_token = context.session.get("oidc_id_token")
    token_decoded = {}
    try:
        token_decoded = jwt.decode(oidc_id_token, options={"verify_signature": False})
    except Exception:
        logger.error("oidc_id_token is niet valide")

    deploy_date_formatted = None
    if settings.DEPLOY_DATE:
        deploy_date = timezone.datetime.strptime(
            settings.DEPLOY_DATE, "%d-%m-%Y-%H-%M-%S"
        )
        deploy_date_formatted = deploy_date.strftime("%d-%m-%Y %H:%M:%S")

    return {
        "MELDINGEN_URL": settings.MELDINGEN_URL,
        "DEBUG": settings.DEBUG,
        "DEV_SOCKET_PORT": settings.DEV_SOCKET_PORT,
        "GET": context.GET,
        "ABSOLUTE_ROOT": absolute(context).get("ABSOLUTE_ROOT"),
        "OIDC_RP_CLIENT_ID": settings.OIDC_RP_CLIENT_ID,
        "SESSION_STATE": token_decoded.get("session_state"),
        "LOGOUT_URL": reverse("oidc_logout"),
        "LOGIN_URL": f"{reverse('oidc_authentication_init')}?next={absolute(context).get('FULL_URL')}",
        "GIT_SHA": settings.GIT_SHA,
        "APP_ENV": settings.APP_ENV,
        "DEPLOY_DATE": deploy_date_formatted,
    }
