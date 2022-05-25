from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_jinja.views.generic import DetailView, ListView

from apps.movie.models import Anime, Season, Episode


class AnimeListView(ListView):
    """Controller to display List of Anime's"""

    model = Anime
    template_name = "movie/list.jinja"

    def get_queryset(self, ):
        """Display anime's with available seasons"""
        return Anime.objects.annotate(seasons_cnt=Count('seasons')).filter(seasons_cnt__gt=0)


class AnimeDetailView(DetailView):
    """Controller to display Anime View"""
    model = Anime
    template_name = "movie/detail.jinja"

    def get_context_data(self, **kwargs):
        """Adding to context seasons, seasons number list, episode, episodes number list"""
        context = super().get_context_data(**kwargs)

        anime: Anime = self.object

        if "season" in self.kwargs:
            context['season'] = get_object_or_404(Season, anime=anime, number=int(self.kwargs['season']))
        else:
            context['season'] = anime.seasons.order_by('number').first()

        if context['season'].episodes.count() == 0:
            raise Http404()

        context['episode'] = context['season'].episodes.order_by('number').first()

        context['season_list'] = anime.seasons.annotate(episode_cnt=Count("episodes"))\
            .filter(episode_cnt__gt=0)\
            .values_list('number', flat=True)
        context['episode_list'] = context['season'].episodes.values_list('number', flat=True)

        return context
