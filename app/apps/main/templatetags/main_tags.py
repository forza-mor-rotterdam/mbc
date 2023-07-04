import json
from datetime import datetime

from django import template

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
    return json.dumps(value)
