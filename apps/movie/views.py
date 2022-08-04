from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, get_language
from django_filters.views import FilterView
from django_jinja.views.generic import DetailView

from apps.movie.constants import AnimeType
from apps.movie.filters import AnimeFilter
from apps.movie.forms import ReviewForm
from apps.movie.models import Anime, Season, Subscribe, MovieSettings
from shared.mixins.breadcrumbs import BreadCrumbsMixin
from shared.mixins.paginator import RemovePageMixin


class AnimeListView(RemovePageMixin, BreadCrumbsMixin, FilterView):
    """Controller to display List of Anime's"""

    model = Anime
    template_name = "movie/list.jinja"
    filterset_class = AnimeFilter

    def get(self, *args, **kwargs):
        """Set settings and paginate_by property"""
        self.settings = MovieSettings.get_solo()
        self.paginate_by = self.settings.movie_per_page
        return super().get(*args, **kwargs)

    def get_breadcrumbs(self):
        return [(_("Home"), reverse("home")), (_("Anime"),)]

    def get_queryset(self):
        """Display anime with available seasons if there are episodes"""
        return Anime.objects.get_lang_queryset().annotate(seasons_cnt=Count('seasons')) \
            .filter(seasons_cnt__gt=0, lang=get_language()).order_by('rating')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = self.settings
        return context


class AnimeDetailView(BreadCrumbsMixin, DetailView):
    """Controller to display Anime View"""
    model = Anime
    template_name = "movie/detail.jinja"

    def get_queryset(self):
        return Anime.objects.get_lang_queryset().annotate(seasons_cnt=Count('seasons')) \
            .filter(seasons_cnt__gt=0, lang=get_language()).order_by('rating')

    def get_breadcrumbs(self):
        return [(_("Home"), reverse("home")), (_("Anime"), reverse("movie:home")), (self.object.name,)]

    def get_context_data(self, **kwargs):
        """Adding to context seasons, seasons number list, episode, episodes number list"""
        context = super().get_context_data(**kwargs)

        anime: Anime = self.object

        if anime.type == AnimeType.FILM:
            context['season'] = anime.seasons.first()
        else:
            if "season" in self.kwargs:
                context['season'] = get_object_or_404(Season, anime=anime, number=int(self.kwargs['season']))
            else:
                context['season'] = anime.seasons.order_by('number').first()

        context['season_list'] = anime.seasons.values_list('number', flat=True)
        context['episode_list'] = context['season'].episodes.values('number', 'pk')

        context['reviews'] = context['season'].reviews.select_related("user").order_by("-datetime")

        context["settings"] = MovieSettings.get_solo()
        context["film_type"] = anime.type

        if self.request.user.is_authenticated:
            context['form'] = ReviewForm()

            if anime.type == AnimeType.SERIAL:
                context['subscribe'] = Subscribe.objects.filter(anime=anime, user=self.request.user).exists()

            rating = self.request.user.ratings.filter(anime=anime).first()
            if rating:
                context['rating'] = rating.val
            else:
                context['rating'] = -1
        return context