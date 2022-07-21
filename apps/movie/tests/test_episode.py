import tempfile

from django.test import TestCase

from apps.account.models import User
from apps.movie.constants import AnimeType
from apps.movie.forms import EpisodeForm
from apps.movie.models import Anime, Season, Episode, Subscribe


class EpisodeTestCase(TestCase):

    def setUp(self):
        self.anime = Anime.objects.create(name="anime", type=AnimeType.FILM, poster=tempfile.NamedTemporaryFile(suffix=".jpg").name)
        self.season = Season.objects.create(name="1", description="1", number=1, anime=self.anime)
        self.episode = Episode.objects.create(number=1, season=self.season)
        self.user = User.objects.create_superuser("test", "test@gmail.com", "test")

    def test_str(self):
        self.assertEqual(str(self.episode), "Episode 1")

    def test_form_error(self):
        """
        Test changing type anime type from Serial to Film
        """

        form = EpisodeForm(data={
            'number': 2,
            'season': self.season
        })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('__all__', None))

    def test_form(self):

        self.anime.type = AnimeType.SERIAL
        self.anime.save()

        form = EpisodeForm(data={
            'number': 2,
            'season': self.season
        })

        self.assertTrue(form.is_valid())
        self.assertFalse(form.has_error('__all__', None))

    def test_emailing(self):
        Subscribe.objects.create(anime=self.anime, user=self.user)
        Episode.objects.create(number=3, season=self.season)

