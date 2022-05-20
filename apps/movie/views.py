from django.db.models import Count
from django.views.generic import ListView

from apps.movie.models import Anime


class AnimeListView(ListView):
    """Controller to display List of Anime's"""

    model = Anime
    template_name = "movie/list.jinja"

    def get_queryset(self, ):
        """Display anime's with available seasons"""
        return Anime.objects.annotate(seasons_cnt=Count('seasons')).filter(seasons_cnt__gt=0)
