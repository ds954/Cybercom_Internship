from django.urls import path
from .views import UserCreateList,UserUpdate

urlpatterns = [
    path("user/",UserCreateList.as_view(),name="user"),
    path("user/<int:pk>",UserUpdate.as_view(),name="user-update"),
]




