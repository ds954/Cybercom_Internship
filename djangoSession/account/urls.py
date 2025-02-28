

from django.urls import path
from .views import *

urlpatterns = [
    path('account/register',RegistrationView.as_view(),name='register'),
    path('account/activate/<str:uid>/<str:token>/',ActivateView.as_view(),name='activate'),
    path('account/activate/',ActivationConfirm.as_view(),name='activation'),
    path('account/csrf_token/',GetCSRFToken.as_view(),name='csrf'),
    path('account/login/',LoginView.as_view(),name='login'),
    path('account/logout/',LogoutView.as_view(),name='logout')
]
