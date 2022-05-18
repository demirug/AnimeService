from jinja2 import Environment


def environment(**options):
    options['cache_size'] = 0
    env = Environment(**options)

    return env
