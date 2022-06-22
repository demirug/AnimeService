from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_jinja.views.generic import DetailView
from apps.textpage.models import TextPage
from shared.mixins.breadcrumbs import BreadCrumbsMixin


class TextPageDetailView(BreadCrumbsMixin, DetailView):
    """TextPage detail view"""
    model = TextPage
    template_name = "textpage/page.jinja"

    def get_breadcrumbs(self):
        return [(_("Home"), reverse("home")), (self.object.name,)]

    def get_queryset(self):
        return TextPage.objects.filter(draft=False)
