import tempfile

from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from apps.movie.admin import AnimeAdmin
from apps.movie.forms import AnimeForm
from apps.movie.models import Anime, Tag
from apps.movie.views import AnimeDetailView


class AnimeTestCase(TestCase):

    def setUp(self):
        self.poster = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.anime_1 = Anime.objects.create(name="Anime-1", poster=self.poster)
        self.anime_2 = Anime.objects.create(name="Anime-1", poster=self.poster)

        self.user = get_user_model().objects.create_superuser(username="test", email="test@gmail.com",
                                                              password="testPass")
        self.client = Client()

    def test_str(self):
        self.assertEqual(str(self.anime_1), self.anime_1.name)

    def test_generated_slug(self):
        self.assertIsNotNone(self.anime_1.slug)

    def test_generated_same_slug(self):
        self.assertEqual(self.anime_2.slug, "anime-1-2")

    def test_absolute_url(self):
        self.assertEqual(self.anime_1.get_absolute_url(), f"/{settings.LANGUAGE_CODE}/anime/anime-1/")

    def test_page(self):
        """Test page by GET request"""

        # Check controller
        response = self.client.get(self.anime_1.get_absolute_url())

        self.assertEqual(response.resolver_match.func.__name__, AnimeDetailView.as_view().__name__)

    def test_admin_save_model(self):
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
