import json
from channels.generic.websocket import WebsocketConsumer

from apps.account.models import User
from asgiref.sync import async_to_sync

MESSAGES_HISTORY_LENGTH = 20

last_messages = []


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_group_name = "chat"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You have been connected'
        }))

        for i in range(len(last_messages)):
            self.send(text_data=last_messages[i])

    def receive(self, text_data):
        user: User = self.scope["user"]
        if not user.is_authenticated:
            return

        text_data_json = json.loads(text_data)

        message = json.dumps({
            'type': 'chat',
            'username': user.username,
            'avatar': user.get_avatar(),
            'message': text_data_json["message"]
        })

        last_messages.append(message)
        if len(last_messages) > MESSAGES_HISTORY_LENGTH:
            del last_messages[0]

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        self.send(text_data=event['message'])
