from django.urls import path
from .consumers import BorrowRequestConsumer

websocket_urlpatterns = [
    path("ws/borrow_request/", BorrowRequestConsumer.as_asgi()),
]
