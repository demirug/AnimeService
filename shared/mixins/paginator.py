class RemovePageMixin:

    def get_context_data(self, *args, **kwargs):
        """Generate GET path with removed paginator attrs"""
        context = super().get_context_data(*args, **kwargs)

        path_no_page = "?%s&" % ''.join([f"{key}={value}&" for key, value in self.request.GET.items()
                                        if key != self.page_kwarg])[:-1]
        context["path"] = path_no_page

        return context