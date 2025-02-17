from django.contrib import admin  
from django.urls import path  
from . import views  
from django.contrib.auth import views as auth_view

urlpatterns = [  
     
     path('register/', views.index), 
     path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
     path('login/', views.login_user, name='login'),
     path('index/',views.student_form_view),
     path('home/',views.home),
     path('enter_email/',views.enter_email,name='enter_email'),
     path('otp/<int:user_id>/',views.otp_password,name='otp'),
     path('reset_password/<int:user_id>/',views.reset_password,name='reset_password'),
     path('reset_password/',auth_view.PasswordResetView.as_view(),name='reset_password'),
     path('reset_password_sent/',auth_view.PasswordResetDoneView.as_view(),name='password_reset_done'),
     path('reset/<uidb64>/<token>',auth_view.PasswordResetConfirmView.as_view(success_url='/login/'),name='password_reset_confirm'),
     path('reset_password_complete/',auth_view.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]  