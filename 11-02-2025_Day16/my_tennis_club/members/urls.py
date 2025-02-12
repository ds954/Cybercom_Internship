from django.urls import path
from . import views

urlpatterns = [
    path('',views.main,name='main'),
    path('members/',views.members,name='hello'),
    path('members/', views.members, name='member'),
    path('members/details/<int:id>', views.details, name='details'),
    path('testing/', views.testing, name='testing'),
    path('tags/',views.tags,name='tags'),
    path('abc/',views.home,name='home'),
    path('car/',views.car),
    path('filter/',views.filter),
    path('edit/<int:member_id>/', views.edit_member, name='edit_member'),
]

