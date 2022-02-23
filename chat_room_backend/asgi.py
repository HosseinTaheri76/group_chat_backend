"""
ASGI config for chat_room_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator
from chat.routing import websocket_urlpatterns as chat_routes
from chat.middleware import TokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_room_backend.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': OriginValidator(
            TokenAuthMiddleware(
                URLRouter(chat_routes)
            ),
            ["*"]
        )
    }
)
