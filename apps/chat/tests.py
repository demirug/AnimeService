import json

from channels.testing import WebsocketCommunicator
from django.test import TestCase
from django.urls import reverse

from apps.account.models import User
from apps.chat.consumers import ChatConsumer
from apps.chat.views import ChatView


class ChatTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="test", email="test@gmail.com", password="test")

    def test_page(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse("chat"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, ChatView.as_view().__name__)

    async def test_connection_establish(self):
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/chat/")
        communicator.scope["user"] = self.user

        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        await communicator.send_to(text_data=json.dumps({}))
        response = await communicator.receive_from()

    async def test_chat(self):
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/chat/")
        communicator.scope["user"] = self.user

        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        await communicator.receive_from()

        await communicator.send_to(text_data=json.dumps({'message': 'hello world'}))
        response = await communicator.receive_from()
        self.assertEqual(response, json.dumps(
            {"type": "chat", "username": "test", "avatar": "/static/account/images/default_avatar.png",
             "message": "hello world"}))
