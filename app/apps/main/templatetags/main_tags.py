import json
import os
from datetime import datetime

import requests
from django import template
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.cache import cache
from requests import Request, Response

register = template.Library()


@register.filter
def to_date(value):
    if not value:
        return
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")
    except Exception as e:
        print(e)
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")


@register.filter
def json_encode(value):
    if isinstance(value, Point):
        return value.geojson
    return json.dumps(value)


@register.filter(name="python_any")
def python_any(values):
    if values:
        return any(values)
    return values


@register.filter
def file_exists(file_path):
    return os.path.isfile(
        os.path.join(settings.BASE_DIR, "apps/main/templates/", file_path)
    )


@register.filter("startswith")
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter("get_svg_path")
def get_svg_pathl(url):
    method = "get"
    action: Request = getattr(requests, method)
    cache_timeout = 60 * 60

    try:
        cache_key = url
        response = cache.get(url)
        if not response:
            response: Response = action(url=url)

            if int(response.status_code) == 200:
                cache.set(cache_key, response, cache_timeout)

        if response:
            return response.text
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


@register.filter("get_last_n_characters")
def get_last_n_characters(string, n=3):
    last_n_characters = string[-n:]
    return last_n_characters
