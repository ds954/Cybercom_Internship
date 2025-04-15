from django.urls import path
from . import views
from API.views import UserCreateList,UserUpdate 
urlpatterns = [
    path('home/', views.index, name="index"),
    path('',views.notification_page,name='notification_page'),
]
