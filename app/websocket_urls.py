from django.urls import path

from apps.chat.consumers import ChatConsumer

urlpatterns = [
    path('chat/', ChatConsumer.as_asgi()),
]