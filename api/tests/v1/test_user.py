from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.account.models import User


class UserTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username="test", email="test@gmail.com", password="test")
        self.client = APIClient()

    def test_user_current(self):
        url = reverse("api:v1:user")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="test", password="test")

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"pk": 1, "username": "test", "email": "test@gmail.com", "avatar": None})
