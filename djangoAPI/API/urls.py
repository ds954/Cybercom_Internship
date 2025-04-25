from django.urls import path
from .views import UserCreateList,UserUpdate,secure_api,csp_report,CSPReportAPIView,ApiEndpoint,my_view,login_view,dynamic_rate_view,another_view,rate_view,secure_token_proxy,malicious_content_view
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import re_path
from .views import UserMicroserviceView, ProductMicroserviceView

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path("user/",UserCreateList.as_view(),name="user"),
    path("user/<int:pk>",UserUpdate.as_view(),name="user-update"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/secure/', secure_api),
    path('sentry-debug/', trigger_error),
     path('csp-report/',csp_report , name='csp_report'),
     path('csp-report1/',CSPReportAPIView.as_view() , name='csp_report'),
     path('endpoint/',ApiEndpoint.as_view(),name="endpoint"),
     path('logger/',my_view,name="logger"),
     path('login_view/',login_view,name="login_view"),
     path('dynamic/',dynamic_rate_view,name="dynamic"),
     path('rate/',rate_view,name="rate"),
     path('another/',another_view,name="another"),
     path('api/secure-token/', secure_token_proxy, name='secure_token_proxy'),
    #   path('api/auth/', EncryptedAuthView.as_view(), name='encrypted-auth'),
    # re_path(r'(?P<path>.*)', TestProxyView.as_view()),
    path('api/users/', UserMicroserviceView.as_view(), name='user_microservice'),
    path('api/products/', ProductMicroserviceView.as_view(), name='product_microservice'),
    path("malicious/", malicious_content_view,name="malicious"),
]




