from django.test import TestCase
from apps.movie.models import Quality


class QualityTestCase(TestCase):

    def setUp(self):
        self.quality_1080 = Quality.objects.create(name="1080p", default=True)
        self.quality_720 = Quality.objects.create(name="720p")
        self.quality_320 = Quality.objects.create(name="320p")

    def test_str(self):
        self.assertEqual(str(self.quality_1080), "1080p")

    def test_default(self):
        quality_2 = Quality.objects.create(name="2K", default=True)
        self.assertEqual(Quality.objects.filter(default=True).count(), 1)

