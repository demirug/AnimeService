from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView
from django_jinja.views.generic import DetailView

from apps.movie.filters import AnimeFilter
from apps.movie.forms import ReviewForm
from apps.movie.models import Anime, Season, Subscribe, Tag, MovieSettings
from shared.mixins.breadcrumbs import BreadCrumbsMixin


class AnimeListView(BreadCrumbsMixin, FilterView):
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
        return Anime.objects.annotate(seasons_cnt=Count('seasons')) \
            .filter(seasons_cnt__gt=0).order_by('rating')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_tags"] = Tag.objects.annotate(anime_count=Count("anime")).filter(anime_count__gt=0)[:5]
        return context


class AnimeDetailView(BreadCrumbsMixin, DetailView):
    """Controller to display Anime View"""
    model = Anime
    template_name = "movie/detail.jinja"

    def get_breadcrumbs(self):
        return [(_("Home"), reverse("home")), (_("Anime"), reverse("movie:home")), (self.object.name,)]

    def get_context_data(self, **kwargs):
        """Adding to context seasons, seasons number list, episode, episodes number list"""
        context = super().get_context_data(**kwargs)

        anime: Anime = self.object

        if "season" in self.kwargs:
            context['season'] = get_object_or_404(Season, anime=anime, number=int(self.kwargs['season']))
        else:
            context['season'] = anime.seasons.order_by('number').first()

        context['season_list'] = anime.seasons.values_list('number', flat=True)
        context['episode_list'] = context['season'].episodes.values('number', 'pk')

        context['reviews'] = context['season'].reviews.order_by("-datetime")\
            .values("text", "datetime", "user__username")

        context["settings"] = MovieSettings.get_solo()

        if self.request.user.is_authenticated:
            context['form'] = ReviewForm()

            context['subscribe'] = Subscribe.objects.filter(anime=anime, user=self.request.user).exists()

            rating = self.request.user.ratings.filter(anime=anime).first()
            if rating:
                context['rating'] = rating.val
            else:
                context['rating'] = -1
        return context