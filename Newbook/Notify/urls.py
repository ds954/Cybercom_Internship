# library/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('request_book/<int:book_id>/', request_book, name='request_book'),
    path('request_renewal/<int:request_id>/', request_renewal, name='request_renewal'), 
    path('cancel_request/<int:request_id>/', cancel_book, name='cancel_book'), 
    path('return_book/<int:request_id>/', return_book, name='return_book'), 
    path('search/', search, name='search'),
    path('search_results/', search_results, name='search_results'),
]