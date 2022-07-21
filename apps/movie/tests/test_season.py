import tempfile

from django.test import TestCase

from apps.movie.constants import AnimeType
from apps.movie.forms import SeasonForm
from apps.movie.models import Anime, Season


class SeasonTestCase(TestCase):

    def setUp(self):
        self.anime = Anime.objects.create(name="anime", type=AnimeType.FILM, poster=tempfile.NamedTemporaryFile(suffix=".jpg").name)
        self.season = Season.objects.create(name="1", description="1", number=1, anime=self.anime)

    def test_str(self):
        self.assertEqual(str(self.season), f"{self.anime.name} | Season #{self.season.number}")

    def test_form_error(self):
        """
        Test changing type anime type from Serial to Film
        """

        form = SeasonForm(data={
            'name': 'test',
            'description': 'test',
            'number': 2,
            'anime': self.anime})

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('__all__', None))

    def test_form(self):
        self.anime.type = AnimeType.SERIAL
        self.anime.save()
        form = SeasonForm(data={
            'name': 'test',
            'description': 'test',
            'number': 2,
            'anime': self.anime})

        self.assertTrue(form.is_valid())
        self.assertFalse(form.has_error('__all__', None))
