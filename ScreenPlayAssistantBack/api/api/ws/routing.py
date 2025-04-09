# chat/routing.py
from django.urls import re_path

from api.ws.consumers import *

websocket_urlpatterns = [
    re_path(r'ws/$', WSConsumer.as_asgi()),
]
