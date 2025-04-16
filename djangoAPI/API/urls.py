from django.urls import path
from .views import UserCreateList,UserUpdate,secure_api,csp_report
from rest_framework.authtoken.views import obtain_auth_token

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path("user/",UserCreateList.as_view(),name="user"),
    path("user/<int:pk>",UserUpdate.as_view(),name="user-update"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/secure/', secure_api),
    path('sentry-debug/', trigger_error),
     path('csp-report/',csp_report , name='csp_report'),

]




