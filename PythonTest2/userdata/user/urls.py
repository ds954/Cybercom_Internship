from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('all_users/', views.all_user, name='all_user'),
    path('add/', views.add_user, name='add'),
    path('update/<int:user_id>/', views.update_user, name='update_user'),
    path('all_users/<int:user_id>/', views.delete_user, name='delete_user'),
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
    path('logout/', views.logout_user, name='logout'),
]
