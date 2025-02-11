import os

from channels.routing import URLRouter, ProtocolTypeRouter

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_asgi_application = get_asgi_application()

from apps.chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
{
    'http': django_asgi_application, 'websocket': URLRouter(websocket_urlpatterns)
}
)
