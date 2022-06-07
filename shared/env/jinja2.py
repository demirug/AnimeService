from jinja2 import Environment

from shared.template_tags.menu import menu_objects


def environment(**options):
    options['cache_size'] = 0
    env = Environment(**options)
    env.globals.update({
        'menu_objects': menu_objects,
    })
    return env