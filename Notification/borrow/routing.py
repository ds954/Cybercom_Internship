from .consumers import BorrowRequestConsumer
from django.urls import path
websocket_urlpatterns=[
    path('ws/borrow-requests/',BorrowRequestConsumer.as_asgi())
]