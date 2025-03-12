from django.urls import path
from .consumers import BorrowRequestConsumer,NotificationConsumer

websocket_urlpatterns = [
    path("ws/borrow_request/", BorrowRequestConsumer.as_asgi()),
    path("ws/notifications/", NotificationConsumer.as_asgi()),
]
