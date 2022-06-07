from django.template.loader import render_to_string


class BreadCrumbsMixin:

    def get_context_data(self, *args, **kwargs):
        """Adding breadcrumbs to context"""
        context = super().get_context_data(*args, **kwargs)

        context["breadcrumbs"] = render_to_string("breadcrumbs.jinja", context={'breadcrumbs': self.get_breadcrumbs()})

        return context

    def get_breadcrumbs(self):
        """Return array with tuples where first element: name, second: url path"""
        return [("name-1", "path-2"), ("name-2", "path-2")]