
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *
urlpatterns = [
   
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',RegisterView.as_view(),name="register"),
    path('login/',LoginView.as_view(),name="login"),
    path('profile/',profileview.as_view(),name="profile"),
    path('ChangePassword/',ChangePasswordView.as_view(),name="password"),
    path('email/',SendPasswordResetEmailView.as_view(),name="email"),
    path('reset_password/<uid>/<token>/',UserPasswordResetView.as_view(),name="email"),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path('book_list/', BookView.as_view(), name='book_list'),
    path('borrow_request/', BorrowRequestView.as_view(), name='borrow_request'),
]
