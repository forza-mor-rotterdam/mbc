from django import template
from django.conf import settings
from webpack_loader.utils import get_loader

register = template.Library()


def _get_static(asset_name, config="DEFAULT"):
    """
    Equivalent to Django's 'static' look up but for webpack assets.
    :param asset_name: the name of the asset
    :param config: (optional) the name of the configuration
    :return: path to webpack asset as a string
    """
    return "{0}{1}{2}".format(
        settings.PROJECT_URL,
        get_loader(config)
        .get_assets()
        .get("publicPath", getattr(settings, "STATIC_URL")),
        asset_name,
    )


@register.simple_tag
def webpack_static(asset_name, config="DEFAULT"):
    return _get_static(asset_name, config=config)
