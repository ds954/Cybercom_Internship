from django.contrib import admin  
from django.urls import path  
from . import views  
urlpatterns = [  
     
     path('register/', views.index), 
     path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
     path('login/', views.login_user, name='login'),
     path('index/',views.student_form_view),
     path('home/',views.home),
     path('enter_email/',views.enter_email,name='enter_email'),
     path('otp/<int:user_id>/',views.otp_password,name='otp'),
     path('reset_password/<int:user_id>/',views.reset_password,name='reset_password')
]  