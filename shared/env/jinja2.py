from jinja2 import Environment

from shared.template_tags.menu import header_objects, footer_objects


def environment(**options):
    options['cache_size'] = 0
    env = Environment(**options)
    env.globals.update({
        'header_objects': header_objects,
        'footer_objects': footer_objects,
    })
    return env