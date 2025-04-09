# api/asgi.py
import os

import django
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import api.events.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            api.events.routing.websocket_urlpatterns
        )
    ),
})
