from django_jinja.views.generic import DetailView
from apps.textpage.models import TextPage


class TextPageDetailView(DetailView):
    """TextPage detail view"""
    model = TextPage
    template_name = "textpage/page.jinja"

    def get_queryset(self):
        return TextPage.objects.filter(draft=False)
