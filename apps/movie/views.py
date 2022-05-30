from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import BaseFormView
from django_jinja.views.generic import DetailView, ListView

from apps.movie.forms import ReviewForm
from apps.movie.models import Anime, Season, Review


class AnimeListView(ListView):
    """Controller to display List of Anime's"""

    model = Anime
    template_name = "movie/list.jinja"

    def get_queryset(self):
        """Display anime with available seasons if there are episodes"""
        return Anime.objects.annotate(seasons_cnt=Count('seasons'), episodes_cnt=Count('seasons__episodes'))\
            .filter(seasons_cnt__gt=0, episodes_cnt__gt=0)


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

        context['reviews'] = context['season'].reviews.order_by("-datetime").values("text", "datetime", "user__username")

        if self.request.user.is_authenticated:
            context['form'] = ReviewForm(instance=Review.objects.filter(user=self.request.user, season=context['season']).first())

        return context


class ReviewCreateUpdateView(LoginRequiredMixin, BaseFormView):

    form_class = ReviewForm

    def get(self, request, *args, **kwargs):
        return redirect("home")

    def form_valid(self, form: ReviewForm):

        season: Season = get_object_or_404(Season, anime__slug=self.kwargs["slug"], number=self.kwargs["season"])

        Review.objects.update_or_create(
            season=season,
            user=self.request.user,
            defaults={'text': form.cleaned_data['text'], 'verified': False}
        )

        return redirect(season.get_absolute_url())
