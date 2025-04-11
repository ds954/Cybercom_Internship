from django.urls import path
from .consumers import BorrowRequestConsumer,NotificationConsumer

"""
 mapping incoming WebSocket connections to the correct consumer.
"""
websocket_urlpatterns = [
    # converts asynchronous consumer (AsyncWebsocketConsumer) into an ASGI (Asynchronous Server Gateway Interface) application.
    path("ws/borrow_request/", BorrowRequestConsumer.as_asgi()),
    path("ws/notifications/", NotificationConsumer.as_asgi()),
]
