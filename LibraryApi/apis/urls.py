from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ApiViewset,home,UserRegistrationView

# Define the router and register the viewset
router = DefaultRouter()
router.register(r'user', ApiViewset, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')), #includes the rest framework's login and logout urls.
    path('home/',home,name='home'),
     path('register/', UserRegistrationView.as_view(), name='register'),
]
