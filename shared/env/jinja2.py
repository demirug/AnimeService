from django.conf import settings
from jinja2 import Environment

from shared.forms import LanguageForm


def environment(**options):
    options['cache_size'] = 0
    env = Environment(**options)
    env.globals.update({
        'language_form': LanguageForm,
        'site_name': settings.SITE_NAME
    })
    return env
