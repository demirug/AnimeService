from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_jinja.views.generic import ListView, DetailView

from apps.news.models import News, NewsSettings
from shared.mixins.breadcrumbs import BreadCrumbsMixin


class NewsListView(ListView):
    """Display all news with paginator"""
    template_name = "news/list.jinja"
    model = News

    def get(self, *args, **kwargs):
        """Set settings and paginate_by property"""
        self.settings = NewsSettings.get_solo()
        self.paginate_by = self.settings.news_per_page
        return super().get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['settings'] = self.settings
        return data


class NewsDetailView(BreadCrumbsMixin, DetailView):
    """News detail view"""
    template_name = "news/detail.jinja"
    model = News

    def get_breadcrumbs(self):
        return [(_("Home"), reverse("home")), (self.object.name,)]
