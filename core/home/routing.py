from django.urls import path
from .consumers import Notificationconsumer,AdminNotificationConsumer
from .consumers import WSconsumer

websocket_urlpatterns = [
    path('ws/url/', WSconsumer.as_asgi()),
    path('ws/notifications/',Notificationconsumer.as_asgi()),
    path('ws/user_requests/',AdminNotificationConsumer.as_asgi())
]
