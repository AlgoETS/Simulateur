# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import simulation.channels.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simulateur.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'https': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            simulation.channels.routing.websocket_urlpatterns
        )
    ),
})
