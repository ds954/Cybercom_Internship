# library/urls.py
from django.urls import path
from .views import user_dashboard, request_book,request_renewal

urlpatterns = [
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('request_book/<int:book_id>/', request_book, name='request_book'),
    path('request_renewal/<int:request_id>/', request_renewal, name='request_renewal'), 
]