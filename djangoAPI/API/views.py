from rest_framework import generics
from .models import UserInfo
from .Serializers import UserSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.throttling import ScopedRateThrottle
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from rest_framework.views import APIView
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit
from django.http import HttpResponse
from .throttling import PaidUserRateThrottle,FreeUserRateThrottle,UserSpecificRateThrottle,DynamicUserRateThrottle

def user_rate(request, view):
    if hasattr(request, 'user') and request.user.is_authenticated:
        return "4/m" if request.user.is_staff else "2/m"
    return "1/m"  # anonymous fallback

# @ratelimit(key='user', rate=user_rate)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserCreateList(generics.ListCreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserSerializers
    throttle_classes = [DynamicUserRateThrottle]
    throttle_scope = 'user'
    



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserSerializers
    throttle_classes = [PaidUserRateThrottle]
    throttle_scope = 'paid'

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def secure_api(request):
    return Response({'message': 'Hello, Authenticated User!'})


@csrf_exempt
def csp_report(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            print("CSP Report Received:", data)
    except Exception as e:
            print(f"Error: {e}")
    return JsonResponse({'status': 'CSP report received'})
    # return JsonResponse({'error': 'Forced error for testing'}, status=500)


# @csrf_exempt
# def csp_report(request):
#     if request.method == 'POST':
#         # Simulating an error if a certain condition is met
#         if 'blocked-uri' not in request.POST:
#             print("missing blcked-uri")
#             return JsonResponse({'error': 'Missing blocked-uri'}, status=400)
        
#         # Otherwise, process the report as usual
#         return JsonResponse({'message': 'CSP report received successfully'}, status=200)
#     return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


class CSPReportAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            report = json.loads(request.body)
            print("🚨 CSP Violation Detected:")
            print(json.dumps(report, indent=4))
        except Exception as e:
            print(f"Error: {e}")
        return Response({"message": "CSP report received."})

class ApiEndpoint(ProtectedResourceView):
    def get(self,request,*arg,**kwargs):
        return HttpResponse("Protected with OAuth2!")

import logging

logger = logging.getLogger('my_app')  # Get a logger instance for the current module

def my_view(request):
    logger.info("Handling request for my_view")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    try:
        # Some code that might raise an exception
        result = 1 / 0
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        # ... handle the error ...
    logger.debug("Finished processing my_view")
    return HttpResponse("Done")

def login_view(request):
    return render(request,'registrations/login.html')

@ratelimit(key='user', rate='2/m') # 5 requests per minute
def rate_view(request):
    return HttpResponse("Success")

@ratelimit(key='user', rate='2/m') # 10 requests per minute
def another_view(request):
    return HttpResponse("Success")


@ratelimit(key='user', rate=user_rate)
def dynamic_rate_view(request):
    return HttpResponse("Success")