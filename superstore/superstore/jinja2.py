from jinja2 import Environment
from django.urls import reverse
from django.middleware.csrf import get_token
from markupsafe import Markup


def url(viewname, *args, **kwargs):
    if kwargs:
        return reverse(viewname, kwargs=kwargs)
    return reverse(viewname, args=args)


def csrf_field(csrf_token):
    return Markup(f'<input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">')


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        "url": url,
        "csrf_field": csrf_field
    })
    return env
