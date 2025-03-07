from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('otp/<int:user_id>',views.verify_otp,name='verify-otp'),
    path('home/', views.home, name='home'),
    path('email/',views.email,name='email'),
    path('otp/<int:user_id>/',views.otp_password,name='otp'),
    path('reset_password/<int:user_id>/',views.reset_password,name='reset_password'),
    path('edit_profile/',views.edit_profile,name="edit_profile")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
