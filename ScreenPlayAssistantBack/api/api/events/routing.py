# chat/routing.py
from django.urls import re_path

from api.events.consumers import Consumer

websocket_urlpatterns = [
    re_path(r'ws/chat/$', Consumer.as_asgi()),
]