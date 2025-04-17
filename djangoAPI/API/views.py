from rest_framework import generics
from .models import UserInfo
from .Serializers import UserSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


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

from rest_framework.views import APIView
from rest_framework.response import Response
import json

class CSPReportAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            report = json.loads(request.body)
            print("🚨 CSP Violation Detected:")
            print(json.dumps(report, indent=4))
        except Exception as e:
            print(f"Error: {e}")
        return Response({"message": "CSP report received."})
