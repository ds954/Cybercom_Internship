from .views import get_blog
from django.urls import path

urlpatterns=[
    path('blog/',get_blog),
]