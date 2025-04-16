from rest_framework import generics
from .models import UserInfo
from .Serializers import UserSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle


# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class UserCreateList(generics.ListCreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserSerializers
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'user_create'


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserSerializers
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'user_update'

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def secure_api(request):
    return Response({'message': 'Hello, Authenticated User!'})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def csp_report(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("CSP Report Received:", data)
        return JsonResponse({'status': 'CSP report received'})

