import tempfile

from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from apps.movie.admin import AnimeAdmin
from apps.movie.constants import AnimeType
from apps.movie.forms import AnimeForm
from apps.movie.models import Anime, Tag, Season, Episode, Rating
from apps.movie.views import AnimeDetailView, AnimeListView


class AnimeTestCase(TestCase):

    def setUp(self):
        self.poster = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.anime_1 = Anime.objects.create(name="Anime-1", poster=self.poster)
        self.anime_2 = Anime.objects.create(name="Anime-1", poster=self.poster)

        self.user = get_user_model().objects.create_superuser(username="test", email="test@gmail.com",
                                                              password="test")
        self.client = Client()

    def test_str(self):
        self.assertEqual(str(self.anime_1), self.anime_1.name)

    def test_generated_slug(self):
        self.assertIsNotNone(self.anime_1.slug)

    def test_generated_same_slug(self):
        self.assertEqual(self.anime_2.slug, "anime-1-2")

    def test_absolute_url(self):
        self.assertEqual(self.anime_1.get_absolute_url(), f"/{settings.LANGUAGE_CODE}/anime/anime-1/")

    def test_admin_save_model(self):
        """
        Test generating anime tags on model save
        """
        tags = ['a', 'b', 'c', 'd']
        model_admin = AnimeAdmin(model=Anime, admin_site=AdminSite())

        # Testing creating object
        anime = Anime(name="123", poster=self.poster)
        form = AnimeForm(instance=anime, data={'tags': " ".join(tags)})
        form.is_valid()
        model_admin.save_model(obj=anime, request=None, form=form, change=None)

        self.assertEqual(Anime.objects.count(), 3)
        self.assertEqual(Tag.objects.filter(name__in=tags).count(), len(tags))

        # Delete all created tags
        Tag.objects.all().delete()

        # Testing updating object
        form = AnimeForm(instance=self.anime_1, data={'tags': " ".join(tags)})
        form.is_valid()
        model_admin.save_model(obj=self.anime_1, request=None, form=form, change=None)
        self.assertEqual(Tag.objects.filter(name__in=tags).count(), len(tags))

    def test_form(self):
        """
        Test changing type anime type from Serial to Film
        """
        anime = Anime.objects.create(name="1", poster=self.poster)
        season = Season.objects.create(name="1", description="1", number=1, anime=anime)
        Episode.objects.create(number=1, season=season)

        form = AnimeForm(instance=anime, data={
            'name': anime.name,
            'lang': anime.lang,
            'type': 'FI'})

        self.assertTrue(form.is_valid())
        self.assertFalse(form.has_error('type', None))
        form.save()
        self.assertEqual(anime.type, 'FI')

    def test_form_error_multiple_seasons(self):
        """
        Test changing type anime type from Serial to Film
        Blocking of count of season more than 1
        """
        anime = Anime.objects.create(name="Test", poster=self.poster)
        season_1 = Season.objects.create(name="season_1", description="season_1", number=1, anime=anime)
        season_2 = Season.objects.create(name="season_2", description="season_2", number=2, anime=anime)
        form = AnimeForm(instance=anime, data={
            'name': anime.name,
            'lang': anime.lang,
            'type': 'FI'})

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('type', None))

    def test_form_error_multiple_episodes(self):
        """
        Test changing type anime type from Serial to Film
        Blocking of count of episodes more than 1
        """
        anime = Anime.objects.create(name="Test", poster=self.poster)
        season_1 = Season.objects.create(name="season_1", description="season_1", number=1, anime=anime)
        episode_1 = Episode.objects.create(number=1, season=season_1)
        episode_2 = Episode.objects.create(number=2, season=season_1)

        form = AnimeForm(instance=anime, data={
            'name': anime.name,
            'lang': anime.lang,
            'type': 'FI'})

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('type', None))

    def test_list_page(self):
        response = self.client.get(reverse("movie:home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, AnimeListView.as_view().__name__)

    def test_filter_list_page(self):
        """Test list anime with searching with tags"""
        response = self.client.get(reverse("movie:home") + "?search=anime-1/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("movie:home") + "?search=anime-1+%23test")
        self.assertEqual(response.status_code, 200)

        self.anime_1.tag_list.add(Tag.objects.create(name="test"))

        response = self.client.get(reverse("movie:home") + "?search=anime-1+%23test")
        self.assertEqual(response.status_code, 200)

    def test_detail_page(self):
        """Test detail page"""
        self.client.login(username="test", password="test")

        anime = Anime.objects.create(name="Anime", poster=self.poster)
        season = Season.objects.create(name="1", description="1", number=1, anime=anime)
        rating = Rating.objects.create(user=self.user, anime=anime, val=1)

        response = self.client.get(anime.get_absolute_url())
        self.assertEqual(response.resolver_match.func.__name__, AnimeDetailView.as_view().__name__)
        self.assertEqual(response.status_code, 200)

        rating.delete()

        response = self.client.get(season.get_absolute_url())
        self.assertEqual(response.resolver_match.func.__name__, AnimeDetailView.as_view().__name__)
        self.assertEqual(response.status_code, 200)

        anime.type = AnimeType.FILM
        anime.save()

        response = self.client.get(anime.get_absolute_url())
        self.assertEqual(response.resolver_match.func.__name__, AnimeDetailView.as_view().__name__)
        self.assertEqual(response.status_code, 200)
