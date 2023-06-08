from django.conf import settings


def general_settings(context):
    return {
        "DEBUG": settings.DEBUG,
    }
