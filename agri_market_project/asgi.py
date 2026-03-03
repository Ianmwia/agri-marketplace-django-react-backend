"""
ASGI config for agri_market_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agri_market_project.settings')
from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter


#redis channels


#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agri_market_project.settings')

import chat.routing

application = ProtocolTypeRouter({
    'http': get_asgi_application(),

    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),

})
