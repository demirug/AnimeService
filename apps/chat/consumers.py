import json
from channels.generic.websocket import WebsocketConsumer

from apps.account.models import User
from asgiref.sync import async_to_sync


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

    def receive(self, text_data):
        user: User = self.scope["user"]
        if not user.is_authenticated:
            return

        text_data_json = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': json.dumps({
                    'type': 'chat',
                    'username': user.username,
                    'avatar': user.get_avatar(),
                    'message': text_data_json["message"]
                })
            }
        )

    def chat_message(self, event):
        self.send(text_data=event['message'])

