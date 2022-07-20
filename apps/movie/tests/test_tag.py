from django.conf import settings
from django.test import TestCase

from apps.movie.models import Tag


class MovieViewsTestCase(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(name="MyTag", display=True)

    def test_str(self):
        self.assertEqual(str(self.tag), f"#{self.tag.name}")

    def test_absolute_url(self):
        self.assertEqual(self.tag.get_absolute_url(), f"/{settings.LANGUAGE_CODE}/anime/?search=%23{self.tag.name}")
