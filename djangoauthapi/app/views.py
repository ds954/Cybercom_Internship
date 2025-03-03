from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import RefreshTokenModel
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timezone
from .serializers import AppUserSerializer
from .serializers import LoginSerializer
from django.contrib.auth import get_user_model
from django.utils.timezone import now

class GetAccessTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=400)

        try:
            # Fetch refresh token from DB
            token_entry = RefreshTokenModel.objects.get(token=refresh_token)
            
            # Check if token is expired
            if token_entry.expires_at < now():
                return Response({"error": "Refresh token expired"}, status=401)
            
            # Generate new access token
            refresh = RefreshToken(token_entry.token)
            new_access_token = str(refresh.access_token)

            return Response({"access": new_access_token})

        except RefreshTokenModel.DoesNotExist:
            return Response({"error": "Invalid refresh token"}, status=400)

User = get_user_model()

class AppUserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = AppUserSerializer(users, many=True)
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        RefreshTokenModel.objects.create(
            user=user,
            token=str(refresh),
            expires_at=datetime.fromtimestamp(refresh.payload["exp"], tz=timezone.utc)
        )

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })

    
class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        try:
            token_entry = RefreshTokenModel.objects.get(token=refresh_token)
            token_entry.delete()  # Remove token from DB
            return Response({"message": "Logged out successfully."})
        except RefreshTokenModel.DoesNotExist:
            return Response({"error": "Invalid token"}, status=400)

