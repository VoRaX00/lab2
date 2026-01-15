from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

def environment(**options):
    env = Environment(**options)
    # Доступ к static и url в шаблонах Jinja2
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
