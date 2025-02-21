import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import Notify.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Newbook.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(Notify.routing.websocket_urlpatterns)  # Handles WebSocket requests
    ),
})
