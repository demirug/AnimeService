from django.test import TestCase, Client
from django.urls import reverse

from apps.news.models import News
from apps.news.views import NewsListView, NewsDetailView


class NewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.news = News.objects.create(name="test", description="test new", content="it's amazing test news")

    def test_str(self):
        self.assertEqual(str(self.news), self.news.name)

    def test_list_page(self):
        url = reverse("home")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, NewsListView.as_view().__name__)

    def test_detail_page(self):
        url = reverse("news", kwargs={"slug": self.news.slug})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, NewsDetailView.as_view().__name__)