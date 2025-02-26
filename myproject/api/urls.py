from django.urls import path
from api.views import RegisterView, LoginView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='api_register'),  
    path('api/login/', LoginView.as_view(), name='api_login'),  
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('api/logout/', LogoutView.as_view(), name='api_logout'),  
]
