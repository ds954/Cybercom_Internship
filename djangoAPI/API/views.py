import base64
import hashlib
from Crypto.Cipher import AES
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import HttpResponse
import os
from django.conf import settings
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
from .throttling import PaidUserRateThrottle,FreeUserRateThrottle,RoleBasedThrottle
from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled

# def user_rate(request, view):
#     if hasattr(request, 'user') and request.user.is_authenticated:
#         return "4/m" if request.user.is_staff else "2/m"
#     return "1/m"  # anonymous fallback
# gateway/views.py
import requests
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from revproxy.views import ProxyView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

class UserMicroserviceView(APIView):
    def get(self, request):
        response = requests.get('http://localhost:8001/api/user/api/users/')
        print("this is response",response)
        return Response(response.json())
    

class ProductMicroserviceView(APIView):
    def get(self, request):
        response = requests.get('http://localhost:8002/api/products/')
        return Response(response.json())

# class TestProxyView(ProxyView):
#     upstream = 'http://127.0.0.1:3000/'

# views.py
from django.http import HttpResponse

def malicious_content_view(request):
    print("called")
    html = """
    <html>
        <head><title>Malicious Page</title></head>
        <body>
            <h1>This is a suspicious script injection</h1>
            <script>
                alert("🚨 Malicious Script Running!");
                document.body.innerHTML += "<p>Trying to steal data...</p>";
            </script>
        </body>
    </html>
    """
    response = HttpResponse(html, content_type="text/html")

    # Apply STRONG security headers to block cross-origin access
    # response["Cross-Origin-Opener-Policy"] = "same-origin"
    # response["Cross-Origin-Resource-Policy"] = "same-origin"
    # response["Cross-Origin-Embedder-Policy"] = "require-corp"
    response["X-Frame-Options"] = "ALLOWALL" 
    # response["X-Frame-Options"] = "DENY" 
  
    # response["X-Content-Type-Options"]="nosniff"
    response["Access-Control-Allow-Origin"] = "*"
    return response
def malicious_script(request):
    html = """
    <html>
        <body>
            <h2>Malicious Content</h2>
            <script>alert("🚨 Malicious Script Running!");</script>
        </body>
    </html>
    """
    response = HttpResponse(html)
    
    # Comment out these headers to allow embedding
    # response["Cross-Origin-Opener-Policy"] = "same-origin"
    # response["Cross-Origin-Resource-Policy"] = "same-origin"
    # response["Cross-Origin-Embedder-Policy"] = "require-corp"
    response["X-Frame-Options"] = "ALLOWALL" 
    # response["X-Frame-Options"] = "DENY" 
  
    # response["X-Content-Type-Options"]="nosniff"
    response["Access-Control-Allow-Origin"] = "*"
    return response

@authentication_classes([TokenAuthentication])
class UserCreateList(generics.ListCreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserSerializers
    throttle_classes = [RoleBasedThrottle]
    permission_classes=[IsAuthenticated]

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserSerializers
    throttle_classes = [PaidUserRateThrottle]

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

class CSPReportAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            report = json.loads(request.body)
            print(" CSP Violation Detected:")
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

# @ratelimit(key='user', rate='2/m') # 5 requests per minute
def rate_view(request):
    return HttpResponse("Success")

# @ratelimit(key='user', rate='2/m') # 10 requests per minute
def another_view(request):
    return HttpResponse("Success")


# @ratelimit(key='user', rate=user_rate)
def dynamic_rate_view(request):
    return HttpResponse("Success")

BASE_DIR = settings.BASE_DIR
verify_path = os.path.join(BASE_DIR, "localhost.crt")

def decrypt_aes_cbc(cipher_text_base64, key_base64, iv_base64):
    key = base64.b64decode(key_base64)
    iv = base64.b64decode(iv_base64)
    cipher_text = base64.b64decode(cipher_text_base64)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(cipher_text)

    # Remove PKCS7 padding
    pad_len = decrypted[-1]
    decrypted = decrypted[:-pad_len]

    return decrypted.decode("utf-8")

@csrf_exempt
def secure_token_proxy(request):
    print("POST DATA:", request.POST)

    try:
        enc_username = request.POST.get("username")
        enc_password = request.POST.get("password")
        print(f"Encrypted Username: {enc_username.strip()}")
        print(f"Encrypted Password: {enc_password.strip()}")


        key = "aBT5RV2hhL7lSMB/Tv0suAnMed9tdYIQn7MLqbpX37Q="  # base64
        iv = "AAAAAAAAAAAAAAAAAAAAAA=="  # base64 16-byte

        username = decrypt_aes_cbc(enc_username, key, iv)
        password = decrypt_aes_cbc(enc_password, key, iv)

        print("username:", username)
        print("password:", password)

        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": "dXmilM4gr2qb8okFhWBiKNMlsBW0IQ9OF2xGcu9L",
            "client_secret": "eHixGBYIC4pIH0kadjeRLYAuf4ma9VbdX5Ou6zSL03pmAy8J1fM1270lxrZXpZ9m1f0gP16zTciaZDWejeWLYmluWq79B2jWhlkeqUspfNq1pQpZSTciXvrMYUw1opjb"
        }

        # Send POST request to get token
        response = requests.post("https://localhost:8000/o/token/", data=data,verify=verify_path)

        # Return the response from the token endpoint
        return JsonResponse(response.json(), status=response.status_code)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, Throttled) and response is not None:
        wait_seconds = int(exc.wait)
        wait_hours = round(wait_seconds / 3600)
        response.data['detail'] = f"Request was throttled. Try again after {wait_hours} hours."

    return response