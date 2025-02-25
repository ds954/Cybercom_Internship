from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ApiViewset,home,UserRegistrationView,UserLoginView,UserLogoutView

# Define the router and register the viewset
router = DefaultRouter()
router.register(r'user', ApiViewset, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')), #includes the rest framework's login and logout urls.
    path('home/',home,name='home'),
     path('register/', UserRegistrationView.as_view(), name='register'),
     path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
