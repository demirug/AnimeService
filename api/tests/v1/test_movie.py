import tempfile

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.account.models import User
from apps.movie.models import Anime, Season, Review, Rating, MovieSettings


class MovieTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username="test", email="test@gmail.com", password="test")
        self.poster = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.anime = Anime.objects.create(name="Anime-1", poster=self.poster)
        self.client = APIClient()

        self.m_settings = MovieSettings.get_solo()

    def test_anime_list(self):
        url = reverse("api:v1:anime-list")

        Anime.objects.create(name="Anime-1-EN", lang='en', poster=self.poster)
        Anime.objects.create(name="Anime-1-uk", lang='uk', poster=self.poster)

        # Test request to list
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Test request to list with another lang
        response = APIClient(HTTP_ACCEPT_LANGUAGE="uk").get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_anime_random(self):
        url = reverse("api:v1:random-list")

        # Test random not found
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test random anime founded
        Season.objects.create(name="test", description="test", number=1, anime=self.anime)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test random with ignoring not found
        response = self.client.get(reverse("api:v1:random-detail", args=("anime-1",)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_review_create(self):
        url = reverse("api:v1:review-list")
        self.client.login(username="test", password="test")
        season = Season.objects.create(name="test", description="test", number=1, anime=self.anime)

        # Test for short review
        response = self.client.post(url, {'season': season.pk,
                                          'text': ''.join(["K" for i in range(self.m_settings.min_review_length - 1)])})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test for long review
        response = self.client.post(url, {'season': season.pk,
                                          'text': ''.join(["K" for i in range(self.m_settings.max_review_length + 1)])})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test for long review
        response = self.client.post(url, {'season': season.pk,
                                          'text': ''.join(["K" for i in range(self.m_settings.max_review_length)])})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

        # Test for review max count per user
        for i in range(4):
            Review.objects.create(season=season, user=self.user, text="test-text")

        response = self.client.post(url, {'season': season.pk, 'text': 'Normal length review =)'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_subscribe(self):
        url = reverse('api:v1:subscribe-list')
        self.client.login(username="test", password="test")

        # Test subscribe
        response = self.client.post(url, {"anime": self.anime.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['subscribe'], True)

        # Test getting subscribe
        response = self.client.get(reverse("api:v1:subscribe-detail", args=(self.anime.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['subscribe'], True)

        # Test unsubscribe
        response = self.client.post(url, {"anime": self.anime.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['subscribe'], False)

    def test_rating(self):
        url = reverse('api:v1:rating-list')
        self.client.login(username="test", password="test")

        # Test rating creation
        response = self.client.post(url, {"anime": self.anime.pk, "val": self.m_settings.max_rating_val})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertEqual(Rating.objects.count(), 1)

        # Test getting rating
        response = self.client.get(reverse('api:v1:rating-detail', args=(self.anime.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], self.m_settings.max_rating_val)

        # Test rating short value
        response = self.client.post(url, {"anime": self.anime.pk, "val": self.m_settings.min_rating_val - 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test rating big value
        response = self.client.post(url, {"anime": self.anime.pk, "val": self.m_settings.max_rating_val + 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
